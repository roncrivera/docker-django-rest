# Python
import requests
import os

RUNDECK_URL        = os.environ.get('RUNDECK_URL')
RUNDECK_AUTH_TOKEN = os.environ.get('RUNDECK_AUTH_TOKEN')


class Rundeck(object):
    """
    This class wraps the methods to work with Rundeck using its REST API.
    """
    def __init__(self, rundeck_url=RUNDECK_URL, api_token=RUNDECK_AUTH_TOKEN, content_type='application/json'):
        """
        Initialise the slumber object with connection to artefactory
        :param rundeck_url: Rundeck URL
        :param api_token: auth token to access Rundeck API
        :param content_type: content-type for request and response, defaults to 'application/json'
        """
        self.rundeck_url = rundeck_url
        self.api_token = api_token
        self.headers = {}
        self.headers['Content-Type'] = content_type
        self.headers['Accept'] = content_type
        self.api = "{}/selfservice/api/19".format(rundeck_url)
        self.generate_token_response = None
        self.job_response = None

    def generate_token(self, user_id, roles, duration="2h"):
        """
        Generate Temporary auth token to trigger rundeck jobs for a given user.
        This class must be instantiated with an api_token that has permissions to generate a token
        :param user_id: bank id of the user for which token will be generated
        :param roles: role groups for this user, default is user bankid
        :param duration: duration of token validity
        """
        payload = {"user": user_id, "roles": roles , "duration": duration}
        self.headers['X-Rundeck-Auth-Token'] = self.api_token
        self.generate_token_response = requests.post(
            url="{}/tokens".format(self.api),
            json=payload,
            headers=self.headers
        )

    def trigger_job(self, job_id, auth_token=RUNDECK_AUTH_TOKEN, argString=None):
        """
        Triggers a job in Rundeck
        :param job_id: Rundeck job id
        :param auth_token: Auth token to trigger the job
        :param argString: Its a string formed with the list of all arguments required to trigger job.
                          Eg: "-argumentname1 value1 -argumentname2 value2"
        """
        self.headers['X-Rundeck-Auth-Token'] = auth_token
        if argString:
            payload = {"argString": argString}
            self.job_response = requests.post(json=payload,
                                     url= "{}/job/{}/run".format(self.api,job_id),
                                     headers = self.headers)

        else:
            self.job_response = requests.post(url="{}/job/{}/run".format(self.api, job_id),
                                     headers=self.headers)
