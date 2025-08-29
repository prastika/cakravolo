# Palm Oil Monitor

## Overview

Palm Oil Monitor is a Flask-based web application designed for monitoring and managing palm oil plantations using AI-powered census operations. The system provides comprehensive tracking of palm trees, their productivity status, flower and fruit counts, and generates predictive analytics for plantation management. It features role-based access control, real-time monitoring dashboards, and interactive mapping capabilities for plantation visualization.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Bootstrap 5 for responsive UI
- **JavaScript Libraries**: Chart.js for data visualization, Leaflet for interactive mapping
- **Styling**: Custom CSS with CSS variables for theming, Bootstrap components for layout
- **Client-side Features**: Real-time data refresh, interactive charts, map clustering for tree locations

### Backend Architecture
- **Framework**: Flask with modular route organization
- **Authentication**: Flask-Login for session management with role-based access (admin, manager, viewer)
- **Database ORM**: SQLAlchemy with declarative base model approach
- **Session Management**: Server-side sessions with configurable secret keys
- **Middleware**: ProxyFix for handling reverse proxy headers

### Data Storage Solutions
- **Primary Database**: SQLite for development with PostgreSQL production support via DATABASE_URL
- **Connection Pooling**: Configured with pool recycling and pre-ping health checks
- **Schema Design**: Relational model with User, Company, CensusOperation, CensusData, and PalmTree entities
- **Data Relationships**: Foreign key relationships between census operations and their associated data

### Authentication and Authorization
- **User Authentication**: Password hashing using Werkzeug security utilities
- **Role-based Access**: Three-tier role system (admin, manager, viewer) with route-level protection
- **Session Security**: Configurable session secrets with environment variable support
- **Login Management**: Automatic redirect to requested pages after authentication

### AI and Analytics Integration
- **Census Operations**: Automated counting of palm flowers and fruits using AI
- **Predictive Analytics**: Future fruit production estimates based on current census data
- **Image Processing**: Support for tree image analysis and storage
- **Recommendation Engine**: Action recommendations based on census results and AI analysis

## External Dependencies

### Core Framework Dependencies
- **Flask**: Web application framework with SQLAlchemy integration
- **Flask-Login**: User session and authentication management
- **Werkzeug**: WSGI utilities and security helpers

### Frontend Libraries
- **Bootstrap 5**: CSS framework for responsive design
- **Font Awesome 6**: Icon library for UI elements
- **Chart.js**: JavaScript charting library for data visualization
- **Leaflet**: Open-source mapping library for plantation visualization

### Database and ORM
- **SQLAlchemy**: Python SQL toolkit and ORM
- **Flask-SQLAlchemy**: Flask integration for SQLAlchemy

### Development and Deployment
- **Python 3**: Runtime environment
- **Environment Variables**: Configuration for database URLs and session secrets
- **ProxyFix**: Werkzeug middleware for reverse proxy support

### Mapping and Geospatial
- **OpenStreetMap**: Base map tiles for plantation mapping
- **ArcGIS/Esri**: Satellite imagery tiles for detailed plantation views
- **Marker Clustering**: Client-side clustering for efficient tree location display