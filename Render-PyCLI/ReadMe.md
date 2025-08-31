# RenderPy

🚀 A Python-based CLI for managing [Render](https://render.com) services, built with **Typer**, **httpx**, **Rich**, and **Textual**.

## Features
- ✅ List services
- ✅ Trigger deployments
- ✅ View deployment history
- ✅ Tail logs with Textual TUI

## Installation
```bash
pip install .
# or if uploaded to PyPI
pip install renderpy
```
## Usage Guide
**Getting Started**  
Before using the CLI, you must authenticate with your Render API key.

*Logging In*  
To save your API key, run the login command. You will be prompted to enter your key, which the CLI will then securely save to a file.

```bash
renderpy login
🔑 Enter Your Render API key:**************
API key saved sucessfully
```

After successfully saving the key, you will see a confirmation message.

**Available Commands**  
The RenderPy CLI provides several commands to interact with your Render services.

**Services**  
These commands help you manage your Render services.  
 * renderpy services list  
   Lists all your Render services in a formatted table, showing the ID, name, type, and status of each.  
 * renderpy services info <service_id>  
   Displays a quick summary for a specific service ID.  
 * renderpy services get <service_id>  
   Displays detailed information for a specific service ID in a formatted table. Use the --json flag to get the raw JSON output instead.    
   Example:
   ```bash
   renderpy services get srv-123abc456def789ghi
   ```  
   Example with JSON output:
   ```bash
   renderpy services get srv-123abc456def789ghi --json
   ```  
   
**Deployments**  
Use these commands to manage deployments for your services.
 * renderpy deploy create <service_id>  
   Triggers a new deployment for the specified service. By default, it uses the main branch. You can specify a different branch with --branch and clear the build cache with --clear-cache.  
  
   Example:
   ```bash
   renderpy deploy create srv-123abc456def789ghi --branch develop --clear-cache
   ```  
 * renderpy deploy list <service_id>  
   Lists all deployments for a given service ID, showing the deployment ID, status, and creation timestamp.  
   
**Logs**  
This command allows you to view the logs for your services in a Textual TUI.  
 * renderpy logs stream <service_id>  
   Streams live logs for a service in real-time. This command replaces the older --tail functionality and provides an interactive TUI. Press Ctrl+C to stop the log stream.    
   Example:
   ```bash
   renderpy logs stream srv-123abc456def789ghi
   ```
