from abc import ABC, abstractmethod


class Interactor[InputDTO, OutputDTO](ABC):
    @abstractmethod
    async def __call__(self, data: InputDTO) -> OutputDTO: ...