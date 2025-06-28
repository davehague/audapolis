import { fetchFromServer } from './index';
import { ServerConfig } from '../state/server';
import { Language, Model } from '../state/models';
import { V1Paragraph, V1V2Silence, V1V2Word } from '../core/document';

export interface Task {
  uuid: string;
}

export enum TranscriptionState {
  QUEUED = 'queued',
  LOADING = 'loading',
  TRANSCRIBING = 'transcribing',
  POST_PROCESSING = 'post_processing',
  DONE = 'done',
  CONVERTING = 'converting',
}

export interface TranscriptionTask extends Task {
  progress: number;
  state: TranscriptionState;
  content?: V1Paragraph<Omit<V1V2Silence | V1V2Word, 'source'>>[];
}

export enum DownloadingModelState {
  QUEUED = 'queued',
  DOWNLOADING = 'downloading',
  EXTRACTING = 'extracting',
  DONE = 'done',
}

export interface DownloadModelTask extends Task {
  lang: string;
  name: string;
  state: DownloadingModelState;
  progress: number;
}

export function startTranscription(
  server: ServerConfig,
  transcription_model: string,
  diarize: boolean,
  diarize_max_speakers: number | null,
  file: File,
  fileName: string
): Promise<TranscriptionTask> {
  const formData: Record<string, any> = { file, fileName, transcription_model, diarize };
  if (diarize_max_speakers !== null) {
    formData['diarize_max_speakers'] = diarize_max_speakers;
  }
  return fetchFromServer(server, 'POST', 'tasks/start_transcription', {}, {
    form: formData,
  })
    .then((x) => x.json())
    .catch((e) => console.error(e));
}

export function downloadModel(server: ServerConfig, model_id: string): Promise<DownloadModelTask> {
  return fetchFromServer(server, 'POST', 'tasks/download_model', { model_id }).then((x) =>
    x.json()
  );
}

export function getTask<T extends Task>(server: ServerConfig, task: T): Promise<T> {
  return fetchFromServer(server, 'GET', `tasks/${task.uuid}`).then((x) => x.json());
}

export function deleteTask(server: ServerConfig, uuid: string): Promise<void> {
  return fetchFromServer(server, 'DELETE', `tasks/${uuid}`).then(() => {});
}

export function deleteModel(server: ServerConfig, model_id: string): Promise<void> {
  return fetchFromServer(server, 'POST', 'models/delete', { model_id }).then(() => {});
}

export function getAvailableModels(server: ServerConfig): Promise<Record<string, Language>> {
  return fetchFromServer(server, 'GET', 'models/available').then((x) => x.json());
}

export function getDownloadedModels(server: ServerConfig): Promise<Record<string, Model>> {
  return fetchFromServer(server, 'GET', 'models/downloaded').then((x) => x.json());
}

export interface OtioSegment {
  speaker: string;
  source_file: string;
  source_length: number;
  has_video: boolean;
  source_start: number;
  length: number;
}

export function convertOtio(
  server: ServerConfig,
  name: string,
  adapter: string,
  timeline: OtioSegment[]
): Promise<ArrayBuffer> {
  return fetchFromServer(
    server,
    'POST',
    'util/otio/convert',
    { name, adapter },
    { json: timeline }
  ).then((x) => x.arrayBuffer());
}
