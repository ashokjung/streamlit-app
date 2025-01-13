import unittest
from unittest.mock import patch, MagicMock
from app import create_batch_prediction_job

class TestCreateBatchPredictionJob(unittest.TestCase):

    @patch('app.aiplatform')
    def test_create_batch_prediction_job_success(self, mock_aiplatform):
        # Arrange
        project_id = "test-project"
        region = "us-central1"
        model_id = "test-model"
        gcs_input_uri = "gs://test-bucket/input-file.csv"
        gcs_output_uri = "gs://test-bucket/output-dir/"
        machine_type = "n1-standard-4"
        job_display_name = "test_batch_prediction_job"

        mock_batch_prediction_job = MagicMock()
        mock_batch_prediction_job.resource_name = "test-job-name"
        mock_batch_prediction_job.state = "JOB_STATE_SUCCEEDED"
        mock_aiplatform.BatchPredictionJob.create.return_value = mock_batch_prediction_job

        # Act
        job_name, job_state = create_batch_prediction_job(
            project_id=project_id,
            region=region,
            model_id=model_id,
            gcs_input_uri=gcs_input_uri,
            gcs_output_uri=gcs_output_uri,
            machine_type=machine_type,
            job_display_name=job_display_name,
        )

        # Assert
        self.assertEqual(job_name, "test-job-name")
        self.assertEqual(job_state, "JOB_STATE_SUCCEEDED")
        mock_aiplatform.init.assert_called_once_with(project=project_id, location=region)
        mock_aiplatform.BatchPredictionJob.create.assert_called_once_with(
            job_display_name=job_display_name,
            model_name=f"projects/{project_id}/locations/{region}/models/{model_id}",
            gcs_source=gcs_input_uri,
            gcs_destination_prefix=gcs_output_uri,
            machine_type=machine_type,
            sync=True,
        )

if __name__ == '__main__':
    unittest.main()