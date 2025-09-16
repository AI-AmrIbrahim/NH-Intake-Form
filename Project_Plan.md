
# Project Plan: Medical E-commerce Recommendation System

## 1. Executive Summary

This document outlines the project plan for developing a sophisticated, AI-powered recommendation system for a medical e-commerce platform. The system will provide customers with personalized vitamin and supplement recommendations based on their individual health needs, medical history, and current medications.

The core of the system will be a LangGraph-based orchestration engine that analyzes customer data from Formium intake forms, cross-references it with medical databases for potential drug interactions and contraindications, and filters products from a Shopify store to provide safe and effective recommendations.

This project plan provides a comprehensive roadmap for the data science team, covering technical architecture, implementation details, development phases, compliance considerations, and success metrics. The goal is to create a production-ready system that is safe, reliable, and scalable.

## 2. Technical Architecture

### 2.1. System Architecture Diagram

```
[User] <-> [Streamlit Application] <-> [LangGraph Orchestration Service] -> [Medical/Shopify APIs]
```

**Description:**

1.  **User:** The user interacts with the Streamlit application.
2.  **Streamlit Application:** A single Python application that serves the user-facing questionnaire (intake form) and displays the final recommendations.
3.  **LangGraph Orchestration Service:** The core Python backend that receives data from the Streamlit app. It runs the analysis, connects to external APIs, and generates the personalized recommendations.
4.  **Medical/Shopify APIs:** External services, such as the NIH's drug interaction database and the Shopify API for product information, are called by the LangGraph service.

### 2.2. Technology Stack

*   **Frontend:** Streamlit (for the user-facing intake form and recommendation display)
*   **Backend:** Python with FastAPI (for the API Gateway and other services)
*   **Orchestration:** LangGraph
*   **Database:** PostgreSQL for structured data (user profiles, medical data), and a vector database like Pinecone or Chroma for embeddings.
*   **Deployment:** Docker, Kubernetes, and a cloud provider like AWS or Google Cloud.
*   **Monitoring:** Prometheus, Grafana, and Sentry for error tracking.

### 2.3. Database Schema

**`user_medical_profiles` table:**

| Column | Data Type | Description |
| :--- | :--- | :--- |
| `user_id` | UUID | Primary Key |
| `age` | INTEGER | User's age |
| `sex` | VARCHAR | User's sex |
| `medical_conditions` | JSONB | A list of medical conditions |
| `current_medications` | JSONB | A list of current medications |
| `allergies` | JSONB | A list of allergies |
| `health_goals` | TEXT | User's health goals |
| `created_at` | TIMESTAMP | Timestamp of creation |
| `updated_at` | TIMESTAMP | Timestamp of last update |

**`product_compatibility` table:**

| Column | Data Type | Description |
| :--- | :--- | :--- |
| `product_id` | VARCHAR | Shopify product ID |
| `contraindicated_conditions` | JSONB | Medical conditions for which this product is contraindicated |
| `interacting_medications` | JSONB | Medications that interact with this product |
| `created_at` | TIMESTAMP | Timestamp of creation |
| `updated_at` | TIMESTAMP | Timestamp of last update |

### 2.4. API Architecture

The system will expose a RESTful API with the following endpoints:

*   `POST /api/recommendations`: Submits the user's medical data and returns a list of recommended products.
*   `GET /api/products`: Returns a list of all products from the Shopify store.
*   `GET /api/products/:id`: Returns information about a specific product.

## 3. LangGraph Orchestration Design

The LangGraph workflow will be designed as a state machine with the following nodes:

1.  **Intake Analysis:** This node receives the user's medical data from the Formium form and structures it for further processing.
2.  **Drug Interaction Checking:** This node uses a drug interaction database (e.g., the NIH's RxNav API) to check for potential interactions between the user's current medications and the products in the Shopify store.
3.  **Contraindication Analysis:** This node checks for contraindications between the user's medical conditions and the products.
4.  **Product Filtering:** This node filters out any products that have been identified as potentially harmful.
5.  **Recommendation Generation:** This node takes the filtered product list and generates a personalized recommendation for the user, along with a detailed explanation of why each product was recommended.

## 4. Streamlit Integration

*   **Intake Form:** The intake form will be built directly within the Streamlit application using components like `st.text_input`, `st.selectbox`, and `st.multiselect` to create a dynamic and user-friendly experience.
*   **Data Validation:** Basic data validation will be implemented directly in Python to ensure the user provides information in the correct format.
*   **User Experience:** The Streamlit app will guide the user through the questions one by one, making the process feel conversational and intuitive.

## 5. Shopify Integration

*   **Product Data Synchronization:** A nightly batch job will synchronize the product catalog from Shopify to the system's database.
*   **Real-time Product Filtering:** The LangGraph workflow will filter products in real-time based on the user's medical profile.
*   **Recommendation Display:** The final recommendations will be displayed on the product pages and in a dedicated "Recommended for You" section.

## 6. Medical Data Processing

*   **Drug Interaction Database:** We will integrate with the NIH's RxNav API to check for drug interactions.
*   **Medical Condition Analysis:** We will use a combination of LLMs and rule-based systems to analyze the user's medical conditions and identify potential risks.
*   **Contraindication Checking:** We will maintain a database of contraindications for each product.
*   **Recommendation Scoring:** We will develop a scoring algorithm that ranks recommendations based on their potential effectiveness and safety.

## 7. Aggressive Development Roadmap (8-Week MVP)

To accelerate time-to-market, we will adopt an aggressive 8-week timeline focused on delivering a Minimum Viable Product (MVP) first, followed by a V1 production release.

### Phase 1: MVP Development (4 Weeks)

*   **Week 1: Core Setup & Intake Form**
    *   Set up the Python environment with FastAPI and Streamlit.
    *   Build the user intake form directly in Streamlit.
    *   Implement a script for a one-time import of Shopify product data.
*   **Week 2: Core Recommendation Logic**
    *   Implement the core LangGraph workflow.
    *   Integrate with the NIH's RxNav API for drug interaction checking.
    *   Develop initial rule-based contraindication logic.
*   **Week 3: End-to-End Integration & MVP Deployment**
    *   Connect all components: Streamlit UI -> FastAPI Backend -> LangGraph Engine.
    *   Generate and display basic product recommendations in the Streamlit app.
    *   Deploy the MVP to a staging environment using Docker.
*   **Week 4: Internal Testing & Refinement**
    *   Conduct internal testing and bug fixing.
    *   Refine the recommendation logic with the medical consultant.
    *   Prepare for a limited beta launch.

### Phase 2: V1 Production Release (4 Weeks)

*   **Weeks 5-6: Enhanced Features & Scalability**
    *   Improve the recommendation scoring algorithm based on feedback.
    *   Enhance the Streamlit UI/UX for a more polished feel.
    *   Implement robust logging, monitoring, and alerting.
    *   Set up automated, nightly product data synchronization with Shopify.
*   **Week 7: Compliance & Security Hardening**
    *   Conduct a full HIPAA compliance review and implement all necessary safeguards (encryption, access controls, audit trails).
    *   Perform security testing and harden the application against common vulnerabilities.
*   **Week 8: Production Launch & Handoff**
    *   Deploy the V1 application to production.
    *   Finalize all documentation.
    *   Hand off the project to the maintenance and operations team.

## 8. Implementation Details

### Folder Structure

```
recommendation-ai/
├── data/
├── docs/
├── src/
│   ├── api/
│   ├── core/
│   ├── services/
│   └── utils/
├── tests/
├── Dockerfile
└── package.json
```

### Testing Strategy

*   **Unit Tests:** Each function and module will have its own set of unit tests.
*   **Integration Tests:** We will write integration tests to ensure that the different components of the system work together correctly.
*   **End-to-End Tests:** We will use a framework like Cypress or Selenium to write end-to-end tests that simulate real user scenarios.

## 9. Compliance and Safety

*   **HIPAA Compliance:** We will ensure that the system is fully HIPAA compliant by encrypting all medical data, implementing strict access controls, and maintaining a detailed audit trail.
*   **Medical Disclaimer:** We will display a clear and prominent medical disclaimer on the website, advising users to consult with a healthcare professional before making any changes to their health regimen.

## 10. Performance and Scalability

*   **Caching:** We will use caching to improve the performance of the system, especially for frequently accessed data like product information.
*   **Load Balancing:** We will use a load balancer to distribute traffic across multiple instances of the application.
*   **Database Optimization:** We will optimize our database queries to ensure that they are as efficient as possible.

## 11. Maintenance and Operations

*   **Monitoring:** We will use Prometheus and Grafana to monitor the health and performance of the system.
*   **Alerting:** We will set up alerts to notify us of any critical issues.
*   **User Support:** We will provide a dedicated support channel for users to report any problems or ask questions.

## 12. Code Examples

### LangGraph Workflow Implementation

```python
from langgraph.graph import StateGraph, END

class RecommendationState:
    # ... state definition ...

def intake_analysis(state: RecommendationState):
    # ... implementation ...

def drug_interaction_checking(state: RecommendationState):
    # ... implementation ...

# ... other node implementations ...

workflow = StateGraph(RecommendationState)
workflow.add_node("intake_analysis", intake_analysis)
workflow.add_node("drug_interaction_checking", drug_interaction_checking)
# ... add other nodes ...

workflow.set_entry_point("intake_analysis")
workflow.add_edge("intake_analysis", "drug_interaction_checking")
# ... add other edges ...

app = workflow.compile()
```

## 13. Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
| :--- | :--- | :--- | :--- |
| Inaccurate recommendations | Medium | High | Thorough testing, human oversight, and a robust QA process. |
| Data breach | Low | High | Strong encryption, access controls, and regular security audits. |
| Performance issues | Medium | Medium | Caching, load balancing, and database optimization. |

## 14. Resource Requirements

*   **Data Scientist/Project Lead:** 1
*   **Software Engineers:** 2-3
*   **QA Engineer:** 1
*   **Medical Consultant:** 1 (part-time)

## 15. Success Metrics

*   **Recommendation Accuracy:** The percentage of recommendations that are deemed safe and effective by our medical consultant.
*   **User Satisfaction:** Measured through user surveys and feedback.
*   **Conversion Rate:** The percentage of users who purchase a recommended product.
*   **System Uptime:** The percentage of time that the system is available and operational.

## 16. Current Upload Functionality (Temporarily Removed)

### What the Upload Feature Currently Does:
- **Location**: Lines 168-209 in main.py (removed temporarily)
- **Trigger**: Only appears when user selects "Yes, I have filled out the intake form before"
- **Requirements**: User must load their profile first (enter Profile Code) before upload is enabled
- **Functionality**:
  - Accepts PDF files only via `st.file_uploader()`
  - Generates unique filename: `{user_id}_{original_name}_{uuid}.pdf`
  - Uploads to Supabase Storage bucket called "test-kit-results"
  - Updates user profile with:
    - `test_kit_result_url`: Public URL from Supabase storage
    - `test_kit_result_filename`: Original filename
  - Shows success/error messages to user

### Technical Implementation Details:
- Uses `supabase.storage.from_("test-kit-results").upload()`
- File naming pattern prevents conflicts with UUID
- Profile update uses existing `save_profile()` function
- Error handling for upload failures included

### Why Temporarily Removed:
- PHI (Protected Health Information) removal needed before file processing
- Feature incomplete without proper data sanitization
- Better UX to hide incomplete features

### Future Development Plan:
1. Add PHI detection/removal pipeline
2. Implement secure file processing
3. Add file validation beyond just PDF type checking
4. Consider file size limits
5. Add file management (view/delete uploaded files)
6. Test with various PDF formats and contents

### Code to Re-add Later:
The upload container code (lines 168-209) is preserved in git history for reference when ready to implement properly with PHI handling.
