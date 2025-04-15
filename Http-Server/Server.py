# Import necessary libraries
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# FastAPI is used to create the HTTP server.
# Pydantic is used for data validation of incoming JSON payloads.

# FastAPI intialization
app = FastAPI(title="MSE HTTP-DDS Bridge")

# Placeholder dictionaries for DDS publishers and subscribers.
# Store DDS entities to reuse them between requests
dds_publishers = {}
dds_subscribers = {}

# Define a generic data model for incoming JSON.
# This will later be replaced by models generated from IDL definitions.
class GenericData(BaseModel):
    data: dict  # A dictionary to hold arbitrary JSON data

# POST endpoint to publish data to a DDS topic
@app.post("/topic/{topic_name}")
async def publish_to_topic(topic_name: str, data: GenericData):
    """
    Handles HTTP POST requests to publish data to a specified DDS topic.

    Args:
        topic_name (str): The name of the DDS topic.
        data (GenericData): The JSON payload sent by the HTTP client.

    Returns:
        dict: A success message if the operation is completed successfully.
    """
    try:
        # Add DDS publisher and data conversion logic
        print(f"Received data for topic '{topic_name}': {data.data}")
        
        # Return a success response
        return {"status": "success", "message": f"Data published to topic '{topic_name}'"}
    except Exception as e:
        # Handle any errors that occur during processing
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# GET endpoint to retrieve data from a DDS topic
@app.get("/topic/{topic_name}")
async def read_from_topic(topic_name: str):
    """
    Handles HTTP GET requests to retrieve data from a specified DDS topic.

    Args:
        topic_name (str): The name of the DDS topic.

    Returns:
        dict: The retrieved data in JSON format or an error message if no data is available.
    """
    try:
        # Return dummy data for testing
        # Implement actual DDS subscriber logic
        dummy_data = {"sensor_id": "dummy_sensor", "value": 123.45, "timestamp": 1616784000}
        
        print(f"Retrieved dummy data for topic '{topic_name}': {dummy_data}")
        
        return dummy_data
    except Exception as e:
        # Handle any errors that occur during processing
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Root endpoint to provide basic API information
@app.get("/")
async def root():
    """
    Root endpoint providing information about available endpoints in the API.

    Returns:
        dict: A message with details of available endpoints.
    """
    return {
        "message": "Welcome to MSE HTTP-DDS Bridge API",
        "endpoints": {
            "publish": "/topic/{topic_name} [POST]",
            "subscribe": "/topic/{topic_name} [GET]"
        }
    }

# Startup event handler
@app.on_event("startup")
async def startup_event():
    """
    Event handler triggered when the server starts up.
    
    This function will initialize any necessary resources,
    such as creating DDS participants or setting up connections.
    """
    print("Initializing resources for MSE HTTP-DDS Bridge...")

# Shutdown event handler
@app.on_event("shutdown")
async def shutdown_event():
    """
    Event handler triggered when the server shuts down.

    This function will clean up any resources,
    such as closing DDS connections or releasing memory.
    """
    print("Cleaning up resources for MSE HTTP-DDS Bridge...")

# Run the application
if __name__ == "__main__":
    import uvicorn  
    uvicorn.run(app, host="0.0.0.0", port=8000)
