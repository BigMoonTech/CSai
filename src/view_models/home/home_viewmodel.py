from src.services import user_service
from src.helpers import helper_functions as helpers
from src.services.completion_service import valid_prompt_len, has_no_profanity
from src.view_models.shared.viewmodel_base import ViewModelBase


class HomeViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.total_requests = user_service.get_total_requests()

        self.resp_text = ''  # the value we will send to the textarea named output
        self.ip_address = helpers.get_ip_address()

        if self.ip_address:
            self.user = user_service.get_unregistered_user_by_ip(self.ip_address)

            if self.user is None:
                self.user = user_service.create_unregistered_user(self.ip_address)

        else:
            self.error = 'Problem creating unregistered user. Please login, ' \
                         'register for an account, or try again later.'

        if self.user is not None:
            self.remaining_calls = self.user.remaining_calls

        self.prompt = ''

    def validate(self) -> bool:
        """ Validate the prompt and remaining calls. """

        if self.error is not None:
            return False

        if self.remaining_calls <= 0:
            self.error = 'You have exceeded your free calls. Please register for an account, or login.'
            return False

        if self.prompt is None or self.prompt == '':
            self.error = 'Please enter a valid prompt.'
            return False

        if not valid_prompt_len(self.prompt):
            self.error = 'Cannot exceed 200 characters.'
            return False

        if not has_no_profanity(self.prompt):
            self.error = 'Cannot contain profanity.'
            return False
        return True
