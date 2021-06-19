import aiohttp
import asyncio
import dataclasses
import json

@dataclasses.dataclass()
class ExamResults:
    exam_id: int
    subject: str
    test_mark: int


class EGEClient:
    def __init__(self, cookies: dict):
        """
        Class constructor
        :param cookies: In order to access API we need cookies
        """
        self.__session: aiohttp.ClientSession = aiohttp.ClientSession(cookies=cookies)
        self._endpoint = 'https://checkege.rustest.ru/api/exam'

    async def __get_raw_exam_results(self):
        request = await self.__session.get(self._endpoint)
        if request.status == 200:
            return await request.text()

    async def get_exam_results(self):
        raw_results = json.loads(await self.__get_raw_exam_results())
        result = raw_results['Result']
        exams = result['Exams']

        list_of_exams: list[ExamResults] = list()
        for exam in exams:
            list_of_exams.append(ExamResults(exam['ExamId'], exam['Subject'], exam['TestMark']))

        return list_of_exams

