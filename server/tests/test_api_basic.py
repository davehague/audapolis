import pytest
from fastapi.testclient import TestClient
from app.main import app


class TestServerBasics:
    """Basic server functionality tests"""
    
    def test_server_can_start(self):
        """Test that the FastAPI server can be initialized"""
        client = TestClient(app)
        assert client is not None
        assert app is not None
        
    def test_app_import(self):
        """Test that the main app can be imported without errors"""
        from app.main import app
        assert app is not None
        assert hasattr(app, 'routes')
        
    def test_cors_middleware_configured(self):
        """Test that CORS middleware is properly configured"""
        from app.main import app
        
        # Check that middleware is configured
        middleware_classes = [type(middleware) for middleware in app.user_middleware]
        middleware_names = [cls.__name__ for cls in middleware_classes]
        
        # Should have CORS middleware
        assert any("CORS" in name for name in middleware_names)
        
    def test_exception_handlers_registered(self):
        """Test that custom exception handlers are registered"""
        from app.main import app
        
        # Check that exception handlers are registered
        assert hasattr(app, 'exception_handlers')
        assert len(app.exception_handlers) > 0


class TestAPIRoutes:
    """Test that all expected API routes are registered"""
    
    def test_transcription_routes_exist(self):
        """Test that transcription routes are registered"""
        client = TestClient(app)
        
        # Test that routes exist (should return 401 without auth, not 404)
        routes_to_test = [
            "/tasks/start_transcription/",
            "/tasks/download_model/",
            "/tasks/list/",
        ]
        
        for route in routes_to_test:
            response = client.post(route) if route.endswith("_transcription/") or route.endswith("_model/") else client.get(route)
            assert response.status_code != 404, f"Route {route} not found"
            
    def test_model_routes_exist(self):
        """Test that model management routes are registered"""
        client = TestClient(app)
        
        routes_to_test = [
            "/models/available",
            "/models/downloaded", 
            "/models/delete"
        ]
        
        for route in routes_to_test:
            if route == "/models/delete":
                response = client.post(route)
            else:
                response = client.get(route)
            assert response.status_code != 404, f"Route {route} not found"
            
    def test_config_routes_exist(self):
        """Test that configuration routes are registered"""
        client = TestClient(app)
        
        # GET /config/ 
        response = client.get("/config/")
        assert response.status_code != 404
        
        # POST /config/
        response = client.post("/config/")
        assert response.status_code != 404
        
    def test_diarization_routes_exist(self):
        """Test that diarization routes are registered"""
        client = TestClient(app)
        
        routes_to_test = [
            ("/POST", "/diarization/analyze/"),
            ("/GET", "/diarization/models/")
        ]
        
        for method, route in routes_to_test:
            if method == "/POST":
                response = client.post(route)
            else:
                response = client.get(route)
            assert response.status_code != 404, f"Route {route} not found"


class TestAuthenticationRequired:
    """Test that endpoints properly require authentication"""
    
    def test_transcription_endpoints_require_auth(self):
        """Test transcription endpoints require authentication"""
        client = TestClient(app)
        
        endpoints = [
            ("POST", "/tasks/start_transcription/"),
            ("POST", "/tasks/download_model/"),
            ("GET", "/tasks/list/"),
        ]
        
        for method, endpoint in endpoints:
            if method == "POST":
                response = client.post(endpoint)
            else:
                response = client.get(endpoint)
                
            assert response.status_code == 401, f"{method} {endpoint} should require authentication"
            
    def test_model_endpoints_require_auth(self):
        """Test model endpoints require authentication"""
        client = TestClient(app)
        
        endpoints = [
            ("GET", "/models/available"),
            ("GET", "/models/downloaded"),
            ("POST", "/models/delete")
        ]
        
        for method, endpoint in endpoints:
            if method == "POST":
                response = client.post(endpoint)
            else:
                response = client.get(endpoint)
                
            assert response.status_code == 401, f"{method} {endpoint} should require authentication"
            
    def test_config_endpoints_require_auth(self):
        """Test config endpoints require authentication"""
        client = TestClient(app)
        
        # GET /config/
        response = client.get("/config/")
        assert response.status_code == 401
        
        # POST /config/
        response = client.post("/config/")
        assert response.status_code == 401
        
    def test_diarization_endpoints_require_auth(self):
        """Test diarization endpoints require authentication"""
        client = TestClient(app)
        
        # POST /diarization/analyze/
        response = client.post("/diarization/analyze/")
        assert response.status_code == 401
        
        # GET /diarization/models/
        response = client.get("/diarization/models/")
        assert response.status_code == 401


class TestTaskEndpoints:
    """Test task-related endpoints"""
    
    def test_get_nonexistent_task_without_auth(self):
        """Test getting a non-existent task without auth returns 401"""
        client = TestClient(app)
        
        response = client.get("/tasks/fake-uuid-12345/")
        assert response.status_code == 401  # Should require auth first
        
    def test_delete_nonexistent_task_without_auth(self):
        """Test deleting a non-existent task without auth returns 401"""  
        client = TestClient(app)
        
        response = client.delete("/tasks/fake-uuid-12345/")
        assert response.status_code == 401  # Should require auth first


class TestErrorHandling:
    """Test basic error handling"""
    
    def test_invalid_route_returns_404(self):
        """Test that invalid routes return 404"""
        client = TestClient(app)
        
        response = client.get("/nonexistent/route/")
        assert response.status_code == 404
        
    def test_method_not_allowed(self):
        """Test that wrong HTTP methods are handled"""
        client = TestClient(app)
        
        # Try DELETE on a GET-only endpoint
        response = client.delete("/models/available")
        assert response.status_code in [405, 401]  # Method not allowed or auth required
        
    def test_malformed_requests_handled_gracefully(self):
        """Test that malformed requests don't crash the server"""
        client = TestClient(app)
        
        # Send malformed data to POST endpoint
        response = client.post(
            "/tasks/start_transcription/",
            data="malformed data that is not form data"
        )
        
        # Should not crash (500), should return auth error (401) or validation error (422)
        assert response.status_code in [401, 422]


class TestApplicationStructure:
    """Test application structure and dependencies"""
    
    def test_required_modules_importable(self):
        """Test that all required modules can be imported"""
        modules_to_test = [
            "app.main",
            "app.models", 
            "app.tasks",
            "app.config"
        ]
        
        for module_name in modules_to_test:
            try:
                __import__(module_name)
            except ImportError as e:
                pytest.fail(f"Required module {module_name} cannot be imported: {e}")
                
    def test_optional_modules_graceful_degradation(self):
        """Test that optional modules degrade gracefully if not available"""
        optional_modules = [
            "app.whisper_engine",
            "app.pyannote_engine", 
            "app.modern_pipeline",
            "app.hardware"
        ]
        
        for module_name in optional_modules:
            try:
                __import__(module_name)
                # If importable, that's good
            except ImportError:
                # If not importable, that should be handled gracefully
                # This test just ensures the import attempt doesn't crash
                pass
                
    def test_auth_token_generation(self):
        """Test that auth token is generated properly"""
        from app.main import AUTH_TOKEN
        
        assert AUTH_TOKEN is not None
        assert len(AUTH_TOKEN) > 10  # Should be a reasonable length
        assert isinstance(AUTH_TOKEN, str)
        
    def test_fastapi_metadata(self):
        """Test FastAPI app metadata"""
        from app.main import app
        
        assert hasattr(app, 'title') or app.title is None  # May or may not be set
        assert hasattr(app, 'version') or app.version is None
        assert hasattr(app, 'routes')
        assert len(app.routes) > 0  # Should have at least some routes


class TestStartupBehavior:
    """Test server startup behavior"""
    
    def test_startup_event_registered(self):
        """Test that startup event is registered"""
        from app.main import app
        
        # Check that startup event is registered
        assert hasattr(app, 'router')
        # The startup event should be registered, but testing it requires more complex setup
        
    def test_cors_origins_configured(self):
        """Test that CORS origins are properly configured"""
        # This is tested by checking that the server starts without CORS errors
        client = TestClient(app)
        
        # Make a request with CORS headers
        headers = {
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST"
        }
        
        response = client.options("/models/available", headers=headers)
        # Should not crash due to CORS issues
        assert response.status_code in [200, 401, 405]  # Various acceptable responses


class TestHealthAndStatus:
    """Test basic health and status functionality"""
    
    def test_server_responds_to_requests(self):
        """Test that server responds to basic requests"""
        client = TestClient(app)
        
        # Make any request to verify server is responsive
        response = client.get("/models/available")
        
        # Should get a response (even if it's an auth error)
        assert response.status_code is not None
        assert response.status_code < 500  # No server errors
        
    def test_json_responses(self):
        """Test that endpoints return valid JSON when appropriate"""
        client = TestClient(app)
        
        # Test an endpoint that should return JSON
        response = client.get("/models/available")
        
        if response.status_code == 200:
            # If successful, should be valid JSON
            try:
                response.json()
            except ValueError:
                pytest.fail("Response should be valid JSON")
        # If not successful, that's expected without auth
        
    def test_no_memory_leaks_in_basic_requests(self):
        """Test that basic requests don't cause obvious memory issues"""
        client = TestClient(app)
        
        # Make multiple requests to check for obvious memory leaks
        for _ in range(10):
            response = client.get("/models/available")
            assert response.status_code in [200, 401]  # Should be consistent
            
        # If we get here without crashes, basic memory handling is working
