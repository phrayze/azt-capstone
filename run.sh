echo "Installing Streamlit Dependencies"
echo "..."
python3 -m venv gemini-streamlit
source gemini-streamlit/bin/activate
pip install -r requirements.txt

export GCP_PROJECT=$(gcloud config get-value project)
echo "Project: ${GCP_PROJECT}"
export GCP_REGION=$(gcloud config get-value compute/region)
echo "Region: ${GCP_REGION}"

echo "..."
echo "Running Streamlit Gemini Application"
streamlit run app.py \
  --browser.serverAddress=localhost \
  --server.enableCORS=false \
  --server.enableXsrfProtection=false \
  --server.port 8080

