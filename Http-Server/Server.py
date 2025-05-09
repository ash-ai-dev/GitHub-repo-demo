# Import necessary libraries
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import json

app = FastAPI(title="MSE HTTP-DDS Bridge")

# Placeholder dictionaries for DDS publishers and subscribers
dds_publishers = {}
dds_subscribers = {}

# Sample IDL structures from the MSE project document
# This represents structures that would normally be parsed from IDL files
# In a production implementation, these would be loaded from actual IDL files

# Dictionary to store Pydantic models that match IDL structures
idl_models = {}

# Define Pydantic models for IDL structures from the document example
class A(BaseModel):
    x: float  # float x
    y: bool   # boolean y

class B(BaseModel):
    a: A              # A a
    b: List[int] = Field(..., min_items=3, max_items=3)  # short[3] b
    c: List[str]      # sequence<string> c

# Define example SensorData structure from the project
class SensorData(BaseModel):
    sensor_id: str    # string sensor_id
    value: float      # double value
    timestamp: int    # long timestamp

# Initialize IDL model registry
@app.on_event("startup")
async def startup_event():
    """
    Event handler triggered when the server starts up.
    
    Initializes DDS resources and registers IDL-based models.
    """
    global idl_models
    
    # Register available IDL structures
    idl_models = {
        "A": A,
        "B": B,
        "SensorData": SensorData
    }
    
    print("Initializing resources for MSE HTTP-DDS Bridge...")
    print(f"Registered IDL structures: {list(idl_models.keys())}")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Event handler triggered when the server shuts down.

    Cleans up resources such as DDS connections.
    """
    print("Cleaning up resources for MSE HTTP-DDS Bridge...")

# Validation function for checking if topic and data match IDL definitions
async def validate_idl_structure(topic_name: str, data: Dict[str, Any]):
    """
    Validates that incoming data matches an IDL-defined structure.
    
    Args:
        topic_name: The name of the topic (should match an IDL structure name)
        data: The data to validate against the IDL structure
        
    Returns:
        The validated data object if validation succeeds
        
    Raises:
        HTTPException: If validation fails or the topic doesn't exist
    """
    if topic_name not in idl_models:
        raise HTTPException(
            status_code=400,
            detail=f"Topic '{topic_name}' does not correspond to any known IDL structure. Available structures: {list(idl_models.keys())}"
        )
    
    model_class = idl_models[topic_name]
    
    try:
        # Validate data against the model
        validated_data = model_class(**data)
        return validated_data
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid data format for '{topic_name}': {str(e)}"
        )

# Generic data model for incoming JSON (before validation)
class GenericData(BaseModel):
    data: Dict[str, Any]

# POST endpoint to publish data to a DDS topic with validation
@app.post("/topic/{topic_name}")
async def publish_to_topic(topic_name: str, data: GenericData):
    """
    Handles HTTP POST requests to publish data to a specified DDS topic.
    Validates that the data matches the IDL-defined structure.

    Args:
        topic_name (str): The name of the DDS topic (must match an IDL structure).
        data (GenericData): The JSON payload sent by the HTTP client.

    Returns:
        dict: A success message if the operation is completed successfully.
    """
    try:
        # Validate data against IDL structure
        validated_data = await validate_idl_structure(topic_name, data.data)
        
        print(f"Received validated data for topic '{topic_name}': {validated_data.dict()}")
        
        # This would eventually use DDS publisher logic:
        # 1. Get or create a DDS publisher for the topic
        # 2. Convert JSON to DDS data using generated code
        # 3. Publish to the DDS topic
        
        return {
            "status": "success", 
            "message": f"Data published to '{topic_name}'",
            "validated": True
        }
    except HTTPException as he:
        # Re-raise HTTP exceptions (from validation)
        raise he
    except Exception as e:
        # Handle any other errors
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# GET endpoint to retrieve data from a DDS topic
@app.get("/topic/{topic_name}")
async def read_from_topic(topic_name: str):
    """
    Handles HTTP GET requests to retrieve data from a specified DDS topic.
    Checks if the topic corresponds to a known IDL structure.

    Args:
        topic_name (str): The name of the DDS topic.

    Returns:
        dict: The retrieved data in JSON format.
    """
    try:
        # Check if topic corresponds to a known IDL structure
        if topic_name not in idl_models:
            raise HTTPException(
                status_code=400,
                detail=f"Topic '{topic_name}' does not correspond to any known IDL structure. Available structures: {list(idl_models.keys())}"
            )
        
        # This would eventually use DDS subscriber logic:
        # 1. Get or create a DDS subscriber for the topic
        # 2. Read from the DDS topic
        # 3. Convert DDS data to JSON
        
        # Return example data based on the topic type
        if topic_name == "SensorData":
            dummy_data = {
                "sensor_id": "dummy_sensor",
                "value": 123.45,
                "timestamp": 1616784000
            }
        elif topic_name == "A":
            dummy_data = {
                "x": 1.23e4,
                "y": True
            }
        elif topic_name == "B":
            dummy_data = {
                "a": {"x": 1.23e4, "y": True},
                "b": [4, 5, 6],
                "c": ["foo", "bar"]
            }
        else:
            dummy_data = {}
        
        print(f"Retrieved dummy data for topic '{topic_name}': {dummy_data}")
        
        return dummy_data
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Root endpoint to provide API information
@app.get("/")
async def root():
    """
    Root endpoint providing information about the API and available IDL structures.

    Returns:
        dict: Information about the API and supported structures.
    """
    return {
        "message": "Welcome to MSE HTTP-DDS Bridge API",
        "endpoints": {
            "publish": "/topic/{topic_name} [POST]",
            "subscribe": "/topic/{topic_name} [GET]"
        },
        "supported_structures": list(idl_models.keys()),
        "example_usage": {
            "post_sensordata": {
                "url": "/topic/SensorData",
                "method": "POST",
                "body": {
                    "data": {
                        "sensor_id": "temp_sensor",
                        "value": 25.4,
                        "timestamp": 1620000000
                    }
                }
            }
        }
    }

# Run the application
if __name__ == "__main__":
    import uvicorn  
    uvicorn.run(app, host="0.0.0.0", port=8000)

