# civic-fix
A mobile-first, crowdsourced platform bridging the gap between citizens and municipal authorities. Streamlines real-time reporting, automated routing, and resolution of local civic issues.

1.)Crowdsourced Civic Issue Reporting & Resolution System
A streamlined, mobile-first solution designed to bridge the communication gap between community members and municipal author
ities. This platform empowers citizens to easily report everyday civic issues (like potholes, broken streetlights, or uncollected trash) while providing local governments with a powerful dashboard to prioritize, route, and resolve these reports efficiently.

2.) Background & Problem Statement
Local governments often face challenges in promptly identifying and resolving everyday civic issues due to a lack of effective reporting and tracking mechanisms. Citizens encounter these problems daily, but the friction of reporting them limits municipal responsiveness.

The Solution: This system provides an easy-to-use interface where users can submit real-time reports with photos and GPS locations. On the administrative side, an automated routing engine directs reports to the correct municipal department, tracking the issue from submission to resolution while providing valuable analytics on government responsiveness.

3.) Tech Stack
Frontend & UI
Core: HTML5, CSS3, Vanilla JavaScript

Framework: Bootstrap (for rapid, responsive UI development)

Mapping: Leaflet.js (for interactive city maps and heatmaps)

Backend & API
Language: Python

Framework: FastAPI

Authentication: JWT (JSON Web Tokens)

Data & Storage
Database: MySQL (Local & Railway for production)

Media Storage: Local storage (Dev) / Cloudinary (Prod)

Hosting: Vercel/Netlify (Frontend) | Render (Backend)

4.) Core Features
Citizen Module: 
Frictionless Reporting: Submit issues with title, description, category, and automatic GPS location tagging.

Multimedia Support: Upload photos to provide immediate context.

Live Tracking & Notifications: Track the timeline of submitted reports (Submitted → Acknowledged → In Progress → Resolved).

Admin & Municipal Dashboard: 
Automated Routing: The system automatically assigns reports based on category (e.g., Garbage → Sanitation, Potholes → Public Works).

Interactive City Map: A live map displaying all issue locations, categorized by custom markers and priority zones.

Report Management: Search, filter, and sort reports. Add internal notes and update public-facing statuses.

📈 Analytics
Performance Tracking: Monitor departmental response times and average resolution rates.

Trend Analysis: Visualize reports by category, status, and monthly volume to identify infrastructure pain points.

 System Workflow
Submission: Citizen registers and submits an issue with an image and location.

Processing: Data is stored, and the system calculates a priority score (e.g., Priority Score = Issue Severity + Number of Similar Reports).

Routing: Automatic assignment to the relevant municipal department.

Action: Admin reviews the report and updates the status.

Resolution: Citizen receives real-time updates as the issue is resolved.

Insight: Analytics dashboards update to reflect new resolution metrics.

 Database Architecture
The system relies on a relational schema to maintain data integrity across users, reports, and real-time updates:

Users: Manages citizen and admin credentials, roles, and contact info.

Reports: The core table tracking issue details, geolocation (latitude/longitude), department assignment, and priority.

Status Updates: A timeline table logging every status change and internal comment for auditability.
