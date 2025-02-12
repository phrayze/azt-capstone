echo "Installing Streamlit Dependencies"
echo "..."
python3 -m venv gemini-streamlit
source gemini-streamlit/bin/activate
pip install -r requirements.txt

export GCP_PROJECT=$(gcloud config get-value project)
if [[ -n $GCP_PROJECT ]]
then
    echo "GCP Project is set"
else
    echo "GCP Project is not set"
    exit 1
fi
echo "Project: ${GCP_PROJECT}"

export GCP_REGION=$(gcloud config get-value compute/region)
if [[ -n $GCP_REGION ]]
then
    echo "GCP Region is: "
else
    echo "GCP Region is not set. Setting Default Region"
    export GCP_REGION="europe-west1"
fi
echo "Region: ${GCP_REGION}"

: '
echo "..."
echo "Running Streamlit Gemini Application"
streamlit run app.py \
  --browser.serverAddress=localhost \
  --server.enableCORS=false \
  --server.enableXsrfProtection=false \
  --server.port 8080
'

AR_REPO='gemini-repo'
SERVICE_NAME='lunchaniser-streamlit-app' 
gcloud artifacts repositories create "$AR_REPO" --location="$GCP_REGION" --repository-format=Docker
gcloud builds submit --tag "$GCP_REGION-docker.pkg.dev/$GCP_PROJECT/$AR_REPO/$SERVICE_NAME"

gcloud run deploy "$SERVICE_NAME" \
  --port=8080 \
  --image="$GCP_REGION-docker.pkg.dev/$GCP_PROJECT/$AR_REPO/$SERVICE_NAME" \
  --allow-unauthenticated \
  --region=$GCP_REGION \
  --platform=managed  \
  --project=$GCP_PROJECT \
  --set-env-vars=GCP_PROJECT=$GCP_PROJECT,GCP_REGION=$GCP_REGION
