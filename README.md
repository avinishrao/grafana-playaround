# grafana-playaround

<a name="readme-top"></a>
<h3 align="center" name="readme-top">Grafana Playaround</h3>

  <p align="center">
    An API call that checks for the organization field & email id field in grafana database if it exists or not. This API call aslo logs messages to SNS & Timestream.
</p>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## About The Project
This is an API operation that triggers grafana API using AWS API gateway to check if the organization inserted in the URL query exists or not in the grafana dashboard. Subsequently, it also checks if the email given in the URL query parameter exists or not & if it does not exist then a new user is created with viewer role. The python script also sends error logs to the SNS & request ID with status code to the AWS timestream.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* Python (version >= 3.9)
* AWS Lambda with API, SNS & Timestream
* Terraform

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started


To get a local copy up and running, follow the steps mentioned below.
(These steps are for Windows)

### Prerequisites

* VSCode
* Git Repo
* Terraform installed on your system
* Postman
  ### Installation

1. Clone the repo to your local destination on computer
   ```sh
   git clone https://github.com/avinishrao/grafana-playaround.git
   ```
2. Open cloned project on VS Code or any compatible IDE
3. Open terminal on VS code, navigate to the directory with terraform source code for which you want to configure the setup
4. Before you start the setup, modify the environment variable based on your configuration 
5. Use the following command in the terminal to setup the lambda function connected to the API & SNS.
   ```sh
   terraform init
   ```
   ```sh
   terraform plan
   ```
   ```sh
   terraform apply
   ```

6. Visit AWS console to check if the resource has been created
7. You can use Postman/Browser with your API URL & URL query parameter with GET or POST methods
   ```sh
   https://{your API URL}/?Param = Value
   ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

Python and AWS has been used to write this script.

_For information, please refer to the [Documentation](https://docs.python.org/3/)_

Following libraries have been used in the script.

_For information on 'os', please refer to the [Documentation](https://docs.python.org/3/library/os.html)_

_For information on 'random', please refer to the [Documentation](https://docs.python.org/3/library/random.html)_

_For information on 'time', please refer to the [Documentation](https://docs.python.org/3/library/time.html)_

_For information on 'boto3', please refer to the [Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)_

_For information on 'requests', please refer to the [Documentation](https://requests.readthedocs.io/en/latest/)_

_For information on 'json', please refer to the [Documentation](https://docs.python.org/3/library/json.html)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Email - avinishrao@gmail.com


<p align="right">(<a href="#readme-top">back to top</a>)</p>
