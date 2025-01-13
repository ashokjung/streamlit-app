import streamlit as st
from google.cloud import aiplatform

def create_batch_prediction_job(
    project_id,
    region,
    model_id,
    gcs_input_uri,
    gcs_output_uri,
    machine_type="n1-standard-4",
    job_display_name="batch_prediction_job",
):
    """Create and start a batch prediction job in Vertex AI."""
    aiplatform.init(project=project_id, location=region)

    batch_prediction_job = aiplatform.BatchPredictionJob.create(
        job_display_name=job_display_name,
        model_name=f"projects/{project_id}/locations/{region}/models/{model_id}",
        gcs_source=gcs_input_uri,
        gcs_destination_prefix=gcs_output_uri,
        machine_type=machine_type,
        sync=True,
    )
    return batch_prediction_job.resource_name, batch_prediction_job.state

# Streamlit UI
st.title("Vertex AI Batch Prediction")

# User Inputs
project_id = st.text_input("Project ID", value="your-project-id")
region = st.text_input("Region", value="us-central1")
model_id = st.text_input("Model ID", value="your-model-id")
gcs_input_uri = st.text_input("GCS Input File Path", value="gs://your-bucket-name/input-file.csv")
gcs_output_uri = st.text_input("GCS Output Directory", value="gs://your-bucket-name/output-dir/")
machine_type = st.selectbox(
    "Machine Type",
    options=["n1-standard-4", "n1-standard-8", "n1-standard-16"],
    index=0,
)

if st.button("Start Batch Prediction"):
    try:
        st.info("Starting batch prediction job...")
        
        # Create and start the batch prediction job
        job_name, job_state = create_batch_prediction_job(
            project_id=project_id,
            region=region,
            model_id=model_id,
            gcs_input_uri=gcs_input_uri,
            gcs_output_uri=gcs_output_uri,
            machine_type=machine_type,
            job_display_name="streamlit_batch_prediction",
        )

        st.success(f"Batch prediction job started successfully!")
        st.write(f"Job Name: {job_name}")
        st.write(f"Job State: {job_state}")
        st.write(f"Output will be saved in: {gcs_output_uri}")

    except Exception as e:
        st.error(f"An error occurred: {e}")


