FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose ports for Streamlit and FastMCP
EXPOSE 8501
EXPOSE 8000

# Set environment variables for Streamlit
ENV PYTHONUNBUFFERED=1

# Command to run the FastMCP server in the background and Streamlit in the foreground
CMD ["sh", "-c", "python -m mcp.server & streamlit run frontend/app.py --server.address=0.0.0.0"]
