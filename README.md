# AIWebProject1



## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab.gwdg.de/aiweb24/aiwebproject1.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](https://gitlab.gwdg.de/aiweb24/aiwebproject1/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Set auto-merge](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

## Name
BrainBite - Feed Your Curiosity

## Description
BrainBite is a powerful and user-friendly search engine designed to crawl and index a website with interesting facts. It enables users to search and discover intreresting information through an intuitive web interface.

### Features
- Independent Crawler: Crawls websites and indexes content efficiently.
- Advanced Indexing: Uses the Whoosh library for structured data storage.
- Intelligent Query Parsing: Supports multi-word search queries and ranks results by relevance.
- Error Correction: Provides spelling suggestions for search queries.
- Modern UI Design: Clean and responsive design with intuitive navigation (accessible search interface with Flask)
- Teaser Display: Shows a teaser (first few sentences) of each result for better context.

### Purpose
The project was developed as part of the course "Artificial Intelligence and the Web" by Cognitive Science Students, to apply and internalise the implementation of core components of a search engine.

### Data
The search engine indexes real-world data sourced directly from https://interestingfacts.com/, a website rich in unique and engaging facts across various topics. The content includes fun facts, historical trivia, science insights, and more.

## Installation
### Requirements
- Python-Version: Python 3.9 or higher
- Operating System: Windows, macOS, Linux

### Dependencies
Install required package via requirements.txt:
    ```
    pip install -r requirements.txt
    ```
Dependencies:
- Flask
- Requests
- BeautifulSoup4
- Whoosh

### Installation and Usage
1. Repository cloning:
    ```
    git clone https://github.com/sophiajaeger/aiwebproject2.git
    ```
2. Create and activate virtual environment:
    create a virtual enviroment:
    ```
        python -m venv myenv
    ```

    activate the enviroment:
    ```
        myenv\Scripts\activate  # Windows
        source myenv/bin/activate  # macOS/Linux
    ```
3. Install the required dependencies:
    ```
        pip install -r requirements.txt
    ```
4. Run the Crawler
    ```
    python crawler.py
    ```
    This will crawl and index content from https://interestingfacts.com/
5. Launch the Web Application
    ```
    python app.py
    ```
    Get access to the search engine.
6. Search for Information
- Enter a search query in the search bar
- Explore the search results and suggested corrections

## Deployment
To deploy the project on a demo server:
1. Upload project files to the server.
2. Install dependencies with pip install -r requirements.txt.
3. Run crawler.py to build the index.
4. Start the Flask app with python app.py.

## Support
For issues or inquiries, please contact:
Email: 
- cbehr@uni-osnabrueck.de
- sjeager@uni-osnabrueck.de
- tgrell@uni-osnabrueck.de

### Report Issues
If you have a bug or have an idea for improvement, please report it in here in GitHub Issues: https://github.com/sophiajaeger/aiwebproject2/issues 
When creating an issue, include:
  - detailed description of the problem or suggestion
  - Steps to reproduce the issue (if applicable)
  - optional: Screenshots or error messages 

## Roadmap
### Long-Term Goals could be
- Semantic search: Semantic analysis to improve the search accurancy.
- Available for Mobile: Enhance responsiveness for mobile devices.
- Advanced Filters: Add filtering options by date, category, or relevance.

### Open for new ideas
We welcome for ideas and contributions!
GitHub Issues https://github.com/sophiajaeger/aiwebproject2/issues

## Contributing
If you would like to contribute your own ideas, you are welcome to improve and expand BrainBite! Just follow the guideline:
1. Fork the repository
    - click the "Fork" button at the top right side of this repository to copy
2. Clone the Forked Repository
    - command to clone locally: 
    ```
    git clone https://github.com/sophiajaeger/aiwebproject2.git
    
    ```
3. Set up your enviroment
    - install the required dependencies:
    ```
    pip install -r requirements.txt
    ```
    - set up a virtual environment: 
    ```
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    ```
4. Create a new Branch for changes
    ```
    git checkout -b feature-branch-name
    ```
6. Dont forget to run Tests
7. Commit and push your changes
    - commit and stage your changes locally:
    ```
    git add .
    git commit -m "a short but clear description of your changes"
    ```
    - push all to GitHub:
    ```
    git push
    ```
8. Submit a Pull Request for to propose changes to   the main project
    - a bunner will appear in your repository indicating that your branch is one commit before octocat:main
    - click Contribute and then Open a Pull Request
    - click on Pull Request -> include a clear description of your changes
9. Wait for an acceptance or questions about your Pull Request

A more detailed description can be found at the following link: https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project

## Authors and acknowledgment
Developed by:
- Sophia Jeager
- Charlotte Behr
- Tuyen Grell

Lecturer of the course "Artificial Intelligence and the Web" (Universität Osnabrück): Dr. phil. Tobias Thelen 

## License
This project is licensed under the MIT License.

## Project status
Done!
