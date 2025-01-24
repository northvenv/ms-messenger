from abc import ABC, abstractmethod


class Interactor[InputDTO, OuputDTO](ABC):
    @abstractmethod
    async def __call__(self, data: InputDTO) -> OuputDTO:
        raise NotImplementedError