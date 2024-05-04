from typing import List

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


class StateDataHas(BaseFilter):
    def __init__(self, required_data_keys: List[str]):
        self.required_data_keys = required_data_keys

    async def __call__(self, message: Message, state: FSMContext, *args,
                       **kwargs):
        data = await state.get_data()
        check_out = [key not in list(data.keys()) for key in self.required_data_keys]
        if True in check_out:
            return False

        return True


