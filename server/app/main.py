import base64
import json
import os
from typing import List, Optional

from fastapi import (
    BackgroundTasks,
    Depends,
    FastAPI,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from starlette.status import HTTP_401_UNAUTHORIZED

from .models import (
    DownloadModelTask,
    LanguageDoesNotExist,
    ModelDoesNotExist,
    ModelNotDownloaded,
    ModelTypeNotSupported,
    models,
)
# Temporarily disabled due to build issues with OpenTimelineIO on Apple Silicon
# from .otio import Segment, convert_otio
from .tasks import TaskNotFoundError, tasks
from .transcribe import TranscriptionState, TranscriptionTask, process_audio
from .modern_pipeline import ModernTranscriptionPipeline
from .diarization_bridge import DiarizationEngine
from .pyannote_engine import AdvancedDiarizationResult
from .huggingface_auth import hf_auth_manager
from .config import config

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AUTH_TOKEN = base64.b64encode(os.urandom(64)).decode()


def token_auth(request: Request):
    authorization: str = request.headers.get("Authorization")
    if authorization != f"Bearer {AUTH_TOKEN}":
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Not authorized")
    return authorization


@app.on_event("startup")
def startup_event():
    print(json.dumps({"msg": "server_started", "token": AUTH_TOKEN}), flush=True)


@app.post("/tasks/start_transcription/")
async def start_transcription(
    background_tasks: BackgroundTasks,
    transcription_model: str = Form(...),
    diarize_max_speakers: Optional[int] = Form(None),
    diarize: bool = Form(False),
    diarization_engine: Optional[str] = Form("auto"), # New parameter
    pipeline_mode: Optional[str] = Form("balanced"), # New parameter
    advanced_features: Optional[List[str]] = Form(None), # New parameter
    file: UploadFile = File(...),
    fileName: str = Form(...),
    auth: str = Depends(token_auth),
):
    task = tasks.add(
        TranscriptionTask(
            file.filename,
            TranscriptionState.QUEUED,
        )
    )

    async def run_pipeline():
        try:
            # Read the audio file content
            audio_bytes = await file.read()
            # Convert to numpy array (assuming WAV for simplicity, more robust handling needed for other formats)
            # This part needs to be more robust to handle various audio formats.
            # For now, assuming it's a WAV file that can be directly read by numpy.frombuffer
            # In a real application, you'd use pydub or similar to load and resample.
            import soundfile as sf
            import io
            
            audio_data, sample_rate = sf.read(io.BytesIO(audio_bytes))

            pipeline = ModernTranscriptionPipeline()
            
            # Define a progress callback that updates the task
            def pipeline_progress_callback(message: str):
                task.state = message # Update task state with progress message
                tasks.update(task) # Persist the update

            final_transcription = pipeline.transcribe(
                audio_data=audio_data,
                sample_rate=sample_rate,
                pipeline_mode=pipeline_mode,
                progress_callback=pipeline_progress_callback,
                task_uuid=task.uuid
            )
            task.content = {"segments": [s._asdict() for s in final_transcription]}
            task.state = TranscriptionState.DONE
        except Exception as e:
            task.state = TranscriptionState.FAILED
            task.content = {"error": str(e), "traceback": traceback.format_exc()}
            logger.error(f"Transcription pipeline failed for task {task.uuid}: {e}")
        finally:
            tasks.update(task)

    background_tasks.add_task(run_pipeline)
    return task


@app.post("/tasks/download_model/")
async def download_model(
    background_tasks: BackgroundTasks,
    model_id: str,
    auth: str = Depends(token_auth),
):
    task = tasks.add(DownloadModelTask(model_id))
    background_tasks.add_task(models.download, model_id, task.uuid)
    return task


# FIXME: this needs to be removed / put behind proper auth for security reasons
@app.get("/tasks/list/")
async def list_tasks(auth: str = Depends(token_auth)):
    return sorted(tasks.list(), key=lambda x: x.uuid)


@app.get("/tasks/{task_uuid}/")
async def get_task(task_uuid: str, auth: str = Depends(token_auth)):
    return tasks.get(task_uuid)


@app.delete("/tasks/{task_uuid}/")
async def remove_task(task_uuid: str, auth: str = Depends(token_auth)):
    return tasks.delete(task_uuid)


@app.get("/models/available")
async def get_all_models(auth: str = Depends(token_auth)):
    return models.available


@app.post("/models/delete")
async def delete_model(model_id: str, auth: str = Depends(token_auth)):
    models.delete(model_id)
    return PlainTextResponse("", status_code=200)


@app.get("/models/downloaded")
async def get_downloaded_models(auth: str = Depends(token_auth)):
    return models.downloaded


@app.get("/config/")
async def get_config(auth: str = Depends(token_auth)):
    return config.get_config()


    return config.get_config()


@app.post("/diarization/analyze/")
async def analyze_diarization(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    preview_mode: bool = Form(False),
    auth: str = Depends(token_auth),
):
    task = tasks.add(
        TranscriptionTask(
            file.filename,
            TranscriptionState.QUEUED,
        )
    )

    async def run_diarization_analysis():
        try:
            audio_bytes = await file.read()
            import soundfile as sf
            import io
            
            audio_data, sample_rate = sf.read(io.BytesIO(audio_bytes))

            diarization_engine = DiarizationEngine()
            
            def diarization_progress_callback(message: str):
                task.state = message
                tasks.update(task)

            advanced_result: AdvancedDiarizationResult = diarization_engine.pyannote_diarizer.diarize(
                audio_data=audio_data,
                sample_rate=sample_rate,
                progress_callback=diarization_progress_callback
            )

            # Convert NamedTuples and numpy arrays for JSON serialization
            segments_json = [s._asdict() for s in advanced_result.segments]
            overlapping_regions_json = [s._asdict() for s in advanced_result.overlapping_regions]
            voice_activity_regions_json = [s._asdict() for s in advanced_result.voice_activity_regions]
            speaker_embeddings_json = {k: v.tolist() for k, v in advanced_result.speaker_embeddings.items()}

            task.content = {
                "segments": segments_json,
                "overlapping_regions": overlapping_regions_json,
                "voice_activity_regions": voice_activity_regions_json,
                "speaker_embeddings": speaker_embeddings_json,
            }
            task.state = TranscriptionState.DONE
        except Exception as e:
            task.state = TranscriptionState.FAILED
            task.content = {"error": str(e), "traceback": traceback.format_exc()}
            logger.error(f"Diarization analysis failed for task {task.uuid}: {e}")
        finally:
            tasks.update(task)

    background_tasks.add_task(run_diarization_analysis)
    return task


@app.get("/diarization/models/")
async def get_diarization_models(auth: str = Depends(token_auth)):
    available_models = models.available
    diarization_models_info = []

    for lang, lang_data in available_models.items():
        for model_desc in lang_data.diarization_models:
            is_downloaded = model_desc.is_downloaded()
            auth_status = "N/A"
            if model_desc.type == "diarization":
                auth_status = "Authenticated" if hf_auth_manager.get_token() else "Not Authenticated"

            diarization_models_info.append({
                "model_id": model_desc.model_id,
                "name": model_desc.name,
                "description": model_desc.description,
                "size": model_desc.size,
                "type": model_desc.type,
                "is_downloaded": is_downloaded,
                "auth_status": auth_status,
                "capabilities": [
                    "speaker_diarization",
                    "overlapping_speech_detection",
                    "voice_activity_detection",
                    "speaker_embedding_extraction"
                ] # Hardcoded for now, can be dynamic based on model_desc
            })
    return diarization_models_info


@app.post("/config/")
async def update_config(new_settings: dict, auth: str = Depends(token_auth)):
    try:
        config.update_config(new_settings)
        return {"message": "Configuration updated successfully.", "new_config": config.get_config()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Temporarily disabled due to OpenTimelineIO build issues on Apple Silicon
# @app.post("/util/otio/convert")
# async def convert_otio_http(
#     name: str,
#     adapter: str,
#     timeline: List[Segment],
#     auth: str = Depends(token_auth),
# ):
#     converted = convert_otio(timeline, name, adapter)
#     return PlainTextResponse(converted)


@app.exception_handler(TaskNotFoundError)
async def task_not_found_error_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=404)


@app.exception_handler(LanguageDoesNotExist)
async def language_does_not_exist_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=404)


@app.exception_handler(ModelDoesNotExist)
async def model_does_not_exist_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=404)


@app.exception_handler(ModelNotDownloaded)
async def model_not_downloaded_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=412)


@app.exception_handler(ModelTypeNotSupported)
async def model_type_not_supported(request, exc):
    return PlainTextResponse(str(exc), status_code=412)
