# Tiltfile

# checks
allow_k8s_contexts('docker-desktop')

# extensions
load('ext://dotenv', 'dotenv')

# environment variables
dotenv(".env")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Define the Docker image for the Lambda service
docker_build(
  "lambda",
  ".",
  dockerfile="Dockerfile",
  # entrypoint=["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "main"],
  live_update=[
    sync("./src", "/var/task/src"),
  ]
)

# Define the Lambda service
k8s_yaml(
  blob("""
apiVersion: v1
kind: Pod
metadata:
  name: lambda-service
spec:
  containers:
    - name: lambda
      image: lambda:latest
      ports:
        - containerPort: 8080
      env:
        - name: SUPABASE_URL
          value: "{}"
        - name: SUPABASE_KEY
          value: "{}"
  restartPolicy: Never
  """.format(SUPABASE_URL, SUPABASE_KEY)
  )
)

# Forward the container port 8080 to the host port 3000
k8s_resource(
  workload="lambda-service",
  port_forwards=[
    "18080:8080",
    # "18089:5678"
  ]
)