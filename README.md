Command to build the application. PLease remeber to change the project name and application name

gcloud builds submit --tag gcr.io/engineering-sdre-dash/SDRE-dash --project= engineering-sdre-dash
Command to deploy the application

gcloud run deploy --image gcr.io/engineering-sdre-dash/SDRE-dash --platform managed  --project=engineering-sdre-dash --allow-unauthenticated
