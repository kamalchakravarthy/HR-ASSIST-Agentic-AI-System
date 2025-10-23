## **HR-ASSIST Agentic AI System**
---
HR ASSIST is an Agentic AI system designed to help HR teams automate routine workflows. This example demonstrates automation of the employee onboarding process, streamlining tasks that typically require manual intervention.

In terms of technical architecture, for MCP client I used Claude Desktop and the code base here represents the MCP server with necessary tools that will be used by MCP client 

🛠️ Setup Instructions

To set up and run HR ASSIST, follow these steps:

- Configure claude_desktop_config.json
Add the following configuration to your claude_desktop_config.json file:

    ```json
    {
    "mcpServers": {
        "hr-assist": {
        "command": "C:\\Users\\dhaval\\.local\\bin\\uv",
        "args": [
            "--directory",
            "C::\\code\\atliq-hr-assist",
            "run",
            "server.py"
        ],
        "env": {
            "CB_EMAIL": "YOUR_EMAIL",
            "CB_EMAIL_PWD": "YOUR_APP_PASSWORD"
        }
        }
    }
    }
    ```

- Replace YOUR_EMAIL with your actual email.
- Replace YOUR_APP_PASSWORD with your email provider’s app-specific password (e.g., for Gmail).
- Run `uv init` and `uv add mcp[cli]` as per the video tutorial in the course.  

**Usage**
- Click on the `+` icon and select the `Add from hr-assist` option, and send the request.
- Fill the details for the new employee:

<img src="resources\image.jpg" alt="Claude desktop prompt with fields" style="width:auto;height:300px;padding-left:30px">

Alternatively, you can draft a custom prompt and let the agent take over.


# HR Workflow Automation Assistant (using FastMCP & Claude)

This project is a powerful HR automation assistant built with Python and `FastMCP`. It uses a large language model client (Claude) to understand natural language prompts and execute complex, multi-step HR workflows, such as onboarding new employees, managing tickets, and handling leave requests.

The backend server (`server.py`) exposes a set of tools (e.g., `add_employee`, `send_email`, `create_ticket`) that the LLM can call. The `utils.py` script seeds the in-memory database with realistic dummy data for demonstration.

## ✨ Core Features

* **Employee Management:** Add new employees, get details, find managers, and list direct reports.
* **Email Automation:** Send welcome emails to new hires and notifications to managers.
* **IT Ticketing:** Automatically raise tickets for new equipment (laptops, ID cards, etc.).
* **Meeting Scheduling:** Schedule introductory meetings and other events.
* **Leave Management:** Check balances, apply for leave, and view history.
* **Complex Workflows:** A single prompt, `onboard_new_employee`, chains all these tools together to perform a complete, end-to-end onboarding.

## 🚀 Demonstration: The `onboard_new_employee` Workflow

This is the project's flagship feature. A single prompt kicks off a 5-step process that completely onboards a new hire, from system entry to their first meeting.

Here is a step-by-step walkthrough of the agent in action:

### 1. The Prompt
It all starts with a simple input form in the Claude client, providing the new employee's name and their manager's name.

![User provides initial prompt inputs for onboarding](Resources/Screenshot%202025-10-22%20230639.png)

### 2. The Agent Takes Over
The agent receives the prompt, breaks it down into a plan, and begins executing the steps. It first gets the manager's details and then moves to Step 1: adding the employee to the HRMS.

![Claude outlines the plan, starting with Step 1: Add employee](Resources/Screenshot%202025-10-22%20230658.png)

A closer look at the tool call shows the agent using the manager's ID (`E003`) it found to correctly add the new employee, Kamal.

![Tool call details for Step 1: Add employee](Resources/Screenshot%202025-10-22%20231049.png)

### 3. Step 2 & 3: Sending Notifications
The agent immediately proceeds to Steps 2 and 3: sending the welcome email and notifying the manager.

**Result (Step 2):** The new employee, Kamal, receives a welcome email with his new Employee ID and corporate email address.

![Welcome email sent to the new employee](Resources/Screenshot%202025-10-22%20230920.png)

**Result (Step 3):** Simultaneously, the manager, Ankit Sharma, receives a detailed email informing him of his new team member.

![Notification email sent to the manager](Resources/Screenshot%202025-10-22%20230939.png)

### 4. Step 4: Raising Equipment Tickets
The agent's plan continues. After sending the emails, it gets the new employee's ID (`E011`) from the output of Step 1 and uses it to raise equipment tickets.

![Claude proceeds to Step 4: Raise tickets](Resources/Screenshot%202025-10-22%20230713.png)

Here is a close-up of the agent calling the `create_ticket` tool for a "Bag", automatically filling in the `emp_id` and a standard reason. It does this for all required items (Laptop, ID Card, etc.).

![Tool call details for Step 4: Create ticket for a bag](Resources/Screenshot%202025-10-22%20231123.png)

### 5. Onboarding Complete!
After all 5 steps are successfully executed, the agent presents a final, clean summary to the user. The entire process—from system entry and emails to IT tickets and meeting schedules—is complete.

![Final "Onboarding Complete!" summary from Claude](Resources/Screenshot%202025-10-22%20230733.png)

## 🛠️ Tech Stack

* **Backend Framework:** `FastMCP`
* **Core Logic:** Python
* **AI Client:** Claude
* **Email:** `smtplib` (via `emails.py`)
* **Data:** In-memory dictionaries (seeded by `utils.py`)

## ⚙️ Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/hr-assist-project.git](https://github.com/your-username/hr-assist-project.git)
    cd hr-assist-project
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up environment variables:**
    Create a `.env` file in the root directory and add your email credentials. The `EmailSender` in `server.py` uses these.
    ```.env
    EMAIL=your-email@gmail.com
    APP_PASSWORD=your-google-app-password
    ```

4.  **Run the server:**
    ```bash
    python server.py
    ```

5.  **Connect your client:**
    Point your Claude desktop client to the local `FastMCP` server to start interacting with the HR assistant.
