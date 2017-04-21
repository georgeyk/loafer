import abc


class AbstractProvider(abc.ABC):

    @abc.abstractmethod
    async def fetch_messages(self):
        '''A coroutine that returns a sequence of messages to be processed.
        If no messages are available, this coroutine should return an empty list.
        '''

    @abc.abstractmethod
    async def confirm_message(self, message):
        '''A coroutine to confirm the message processing.
        After the message confirmation we should not receive the same message again.
        This usually means we need to delete the message in the provider.
        '''

    def stop(self):
        '''Stops the provider.
        If needed, the provider should perform clean-up actions.
        This method is called whenever we need to shutdown the provider.
        '''
        pass
