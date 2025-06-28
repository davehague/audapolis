import pytest
import json
from fastapi.testclient import TestClient
from app.main import app


class TestTranscriptionAPI:
    """Test the Audapolis transcription API endpoints"""
    
    def test_start_transcription_requires_auth(self):
        """Test that transcription endpoint requires authentication"""
        client = TestClient(app)
        response = client.post("/tasks/start_transcription/")
        assert response.status_code == 401
        
    def test_start_transcription_with_audio_file(
        self, 
        test_client_with_auth, 
        auth_headers, 
        audio_file, 
        complete_mocked_environment
    ):
        """Test successful transcription with audio file"""
        
        with open(audio_file, "rb") as f:
            files = {"file": ("test.wav", f, "audio/wav")}
            data = {
                "transcription_model": "whisper_tiny",
                "fileName": "test.wav",
                "diarize": False,
                "pipeline_mode": "balanced"
            }
            
            response = test_client_with_auth.post(
                "/tasks/start_transcription/",
                headers=auth_headers,
                files=files,
                data=data
            )
            
        assert response.status_code == 200
        task = response.json()
        assert "uuid" in task
        assert task["filename"] == "test.wav"
        
    def test_start_transcription_with_video_file(
        self,
        test_client_with_auth,
        auth_headers, 
        video_file,
        complete_mocked_environment
    ):
        """Test transcription with video file"""
        
        with open(video_file, "rb") as f:
            files = {"file": ("test-video.mp4", f, "video/mp4")}
            data = {
                "transcription_model": "whisper_tiny",
                "fileName": "test-video.mp4",
                "diarize": True,
                "diarize_max_speakers": 2,
                "diarization_engine": "pyannote"
            }
            
            response = test_client_with_auth.post(
                "/tasks/start_transcription/",
                headers=auth_headers,
                files=files,
                data=data
            )
            
        assert response.status_code == 200
        task = response.json()
        assert "uuid" in task
        assert task["filename"] == "test-video.mp4"
        
    def test_start_transcription_with_diarization(
        self,
        test_client_with_auth,
        auth_headers,
        audio_file,
        complete_mocked_environment
    ):
        """Test transcription with speaker diarization enabled"""
        
        with open(audio_file, "rb") as f:
            files = {"file": ("multi_speaker.wav", f, "audio/wav")}
            data = {
                "transcription_model": "whisper_small",
                "fileName": "multi_speaker.wav", 
                "diarize": True,
                "diarize_max_speakers": 3,
                "diarization_engine": "pyannote",
                "pipeline_mode": "accuracy"
            }
            
            response = test_client_with_auth.post(
                "/tasks/start_transcription/",
                headers=auth_headers,
                files=files,
                data=data
            )
            
        assert response.status_code == 200
        task = response.json()
        assert "uuid" in task
        
    def test_get_task_status(self, test_client_with_auth, auth_headers, complete_mocked_environment):
        """Test getting task status"""
        
        # Test with valid task UUID
        response = test_client_with_auth.get("/tasks/test-task-uuid-123/", headers=auth_headers)
        assert response.status_code == 200
        task = response.json()
        assert "uuid" in task
        assert "state" in task
        
    def test_get_nonexistent_task(self, test_client_with_auth, auth_headers):
        """Test getting non-existent task returns 404"""
        
        response = test_client_with_auth.get("/tasks/nonexistent-uuid/", headers=auth_headers)
        assert response.status_code == 404
        
    def test_list_tasks(self, test_client_with_auth, auth_headers, complete_mocked_environment):
        """Test listing all tasks"""
        
        response = test_client_with_auth.get("/tasks/list/", headers=auth_headers)
        assert response.status_code == 200
        tasks = response.json()
        assert isinstance(tasks, list)
        
    def test_delete_task(self, test_client_with_auth, auth_headers, complete_mocked_environment):
        """Test deleting a task"""
        
        response = test_client_with_auth.delete("/tasks/test-task-uuid-123/", headers=auth_headers)
        assert response.status_code == 200


class TestModelsAPI:
    """Test model management API endpoints"""
    
    def test_get_available_models(self, test_client_with_auth, auth_headers, complete_mocked_environment):
        """Test GET /models/available endpoint"""
        
        response = test_client_with_auth.get("/models/available", headers=auth_headers)
        assert response.status_code == 200
        models = response.json()
        assert isinstance(models, dict)
        assert "en" in models
        
    def test_get_downloaded_models(self, test_client_with_auth, auth_headers, complete_mocked_environment):
        """Test GET /models/downloaded endpoint"""
        
        response = test_client_with_auth.get("/models/downloaded", headers=auth_headers)
        assert response.status_code == 200
        models = response.json()
        assert isinstance(models, list)
        
    def test_download_model(self, test_client_with_auth, auth_headers, complete_mocked_environment):
        """Test model download endpoint"""
        
        response = test_client_with_auth.post(
            "/tasks/download_model/",
            headers=auth_headers,
            data={"model_id": "whisper_tiny"}
        )
        
        assert response.status_code == 200
        task = response.json()
        assert "uuid" in task
        
    def test_delete_model(self, test_client_with_auth, auth_headers, complete_mocked_environment):
        """Test model deletion endpoint"""
        
        response = test_client_with_auth.post(
            "/models/delete",
            headers=auth_headers,
            data={"model_id": "whisper_tiny"}
        )
        
        assert response.status_code == 200


class TestDiarizationAPI:
    """Test diarization-specific API endpoints"""
    
    def test_diarization_analyze_with_audio(
        self,
        test_client_with_auth,
        auth_headers,
        audio_file,
        complete_mocked_environment
    ):
        """Test diarization analysis with audio file"""
        
        with open(audio_file, "rb") as f:
            files = {"file": ("diarization_test.wav", f, "audio/wav")}
            data = {"preview_mode": False}
            
            response = test_client_with_auth.post(
                "/diarization/analyze/",
                headers=auth_headers,
                files=files,
                data=data
            )
            
        assert response.status_code == 200
        task = response.json()
        assert "uuid" in task
        
    def test_diarization_analyze_with_video(
        self,
        test_client_with_auth,
        auth_headers,
        video_file,
        complete_mocked_environment
    ):
        """Test diarization analysis with video file"""
        
        with open(video_file, "rb") as f:
            files = {"file": ("diarization_video.mp4", f, "video/mp4")}
            data = {"preview_mode": True}
            
            response = test_client_with_auth.post(
                "/diarization/analyze/",
                headers=auth_headers,
                files=files,
                data=data
            )
            
        assert response.status_code == 200
        task = response.json()
        assert "uuid" in task
        
    def test_get_diarization_models(self, test_client_with_auth, auth_headers, complete_mocked_environment):
        """Test getting available diarization models"""
        
        response = test_client_with_auth.get("/diarization/models/", headers=auth_headers)
        assert response.status_code == 200
        models = response.json()
        assert isinstance(models, list)


class TestConfigAPI:
    """Test configuration API endpoints"""
    
    def test_get_config(self, test_client_with_auth, auth_headers, complete_mocked_environment):
        """Test getting current configuration"""
        
        response = test_client_with_auth.get("/config/", headers=auth_headers)
        assert response.status_code == 200
        config = response.json()
        assert isinstance(config, dict)
        
    def test_update_config(self, test_client_with_auth, auth_headers, complete_mocked_environment):
        """Test updating configuration"""
        
        new_config = {
            "transcription_engine": "whisper",
            "gpu_acceleration": True
        }
        
        response = test_client_with_auth.post(
            "/config/",
            headers=auth_headers,
            json=new_config
        )
        
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert "new_config" in result


class TestAPIErrorHandling:
    """Test API error handling and edge cases"""
    
    def test_missing_file_parameter(self, test_client_with_auth, auth_headers):
        """Test transcription without file parameter"""
        
        data = {
            "transcription_model": "whisper_tiny",
            "fileName": "test.wav"
        }
        
        response = test_client_with_auth.post(
            "/tasks/start_transcription/",
            headers=auth_headers,
            data=data
        )
        
        assert response.status_code == 422  # Validation error
        
    def test_missing_required_fields(self, test_client_with_auth, auth_headers, audio_file):
        """Test transcription with missing required fields"""
        
        with open(audio_file, "rb") as f:
            files = {"file": ("test.wav", f, "audio/wav")}
            data = {
                # Missing transcription_model and fileName
            }
            
            response = test_client_with_auth.post(
                "/tasks/start_transcription/",
                headers=auth_headers,
                files=files,
                data=data
            )
            
        assert response.status_code == 422
        
    def test_invalid_model_id(self, test_client_with_auth, auth_headers):
        """Test download with invalid model ID"""
        
        response = test_client_with_auth.post(
            "/tasks/download_model/",
            headers=auth_headers,
            data={"model_id": "nonexistent_model_12345"}
        )
        
        # Should handle gracefully (exact response depends on implementation)
        assert response.status_code in [200, 400, 404]
        
    def test_unauthorized_access(self):
        """Test that all endpoints require authentication"""
        client = TestClient(app)
        
        endpoints = [
            ("GET", "/tasks/list/"),
            ("GET", "/models/available"),
            ("GET", "/models/downloaded"),
            ("GET", "/config/"),
            ("GET", "/diarization/models/"),
            ("GET", "/tasks/fake-uuid/"),
        ]
        
        for method, endpoint in endpoints:
            if method == "GET":
                response = client.get(endpoint)
            elif method == "POST":
                response = client.post(endpoint)
                
            assert response.status_code == 401, f"{method} {endpoint} should require auth"
            
    def test_malformed_json_config(self, test_client_with_auth, auth_headers):
        """Test config update with invalid JSON"""
        
        headers_with_json = {**auth_headers, "Content-Type": "application/json"}
        
        response = test_client_with_auth.post(
            "/config/",
            headers=headers_with_json,
            data="invalid json data"  # Not JSON
        )
        
        assert response.status_code in [400, 422]


class TestAPIPerformance:
    """Basic performance and reliability tests"""
    
    @pytest.mark.slow
    def test_concurrent_transcription_requests(
        self,
        test_client_with_auth,
        auth_headers,
        audio_file,
        complete_mocked_environment
    ):
        """Test multiple simultaneous transcription requests"""
        import threading
        
        results = []
        
        def make_request():
            try:
                with open(audio_file, "rb") as f:
                    files = {"file": ("concurrent_test.wav", f, "audio/wav")}
                    data = {
                        "transcription_model": "whisper_tiny",
                        "fileName": "concurrent_test.wav",
                        "diarize": False
                    }
                    
                    response = test_client_with_auth.post(
                        "/tasks/start_transcription/",
                        headers=auth_headers,
                        files=files,
                        data=data
                    )
                    results.append(response.status_code)
            except Exception as e:
                results.append(500)  # Error occurred
        
        # Start 3 concurrent requests
        threads = [threading.Thread(target=make_request) for _ in range(3)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
            
        # All should succeed
        assert len(results) == 3
        assert all(status == 200 for status in results), f"Some requests failed: {results}"
        
    def test_video_file_processing(
        self,
        test_client_with_auth,
        auth_headers,
        video_file,
        complete_mocked_environment
    ):
        """Test that video files are handled properly"""
        
        with open(video_file, "rb") as f:
            files = {"file": ("test-video.mp4", f, "video/mp4")}
            data = {
                "transcription_model": "whisper_tiny",
                "fileName": "test-video.mp4",
                "diarize": True,
                "diarize_max_speakers": 2
            }
            
            response = test_client_with_auth.post(
                "/tasks/start_transcription/",
                headers=auth_headers,
                files=files,
                data=data
            )
            
        # Should handle video files successfully
        assert response.status_code == 200
        task = response.json()
        assert "uuid" in task
        assert task["filename"] == "test-video.mp4"


class TestAPIIntegration:
    """Integration tests for complete workflows"""
    
    def test_complete_transcription_workflow(
        self,
        test_client_with_auth,
        auth_headers,
        audio_file,
        complete_mocked_environment
    ):
        """Test complete workflow: upload → transcribe → get result"""
        
        # Step 1: Start transcription
        with open(audio_file, "rb") as f:
            files = {"file": ("workflow_test.wav", f, "audio/wav")}
            data = {
                "transcription_model": "whisper_tiny",
                "fileName": "workflow_test.wav",
                "diarize": False
            }
            
            response = test_client_with_auth.post(
                "/tasks/start_transcription/",
                headers=auth_headers,
                files=files,
                data=data
            )
            
        assert response.status_code == 200
        task = response.json()
        task_uuid = task["uuid"]
        
        # Step 2: Check task status
        response = test_client_with_auth.get(f"/tasks/{task_uuid}/", headers=auth_headers)
        assert response.status_code == 200
        task_status = response.json()
        assert "state" in task_status
        
        # Step 3: Clean up - delete task
        response = test_client_with_auth.delete(f"/tasks/{task_uuid}/", headers=auth_headers)
        assert response.status_code == 200
        
    def test_model_management_workflow(
        self,
        test_client_with_auth,
        auth_headers,
        complete_mocked_environment
    ):
        """Test model management workflow"""
        
        # Step 1: List available models
        response = test_client_with_auth.get("/models/available", headers=auth_headers)
        assert response.status_code == 200
        
        # Step 2: Check downloaded models
        response = test_client_with_auth.get("/models/downloaded", headers=auth_headers)
        assert response.status_code == 200
        
        # Step 3: Download a model
        response = test_client_with_auth.post(
            "/tasks/download_model/",
            headers=auth_headers,
            data={"model_id": "whisper_tiny"}
        )
        assert response.status_code == 200
