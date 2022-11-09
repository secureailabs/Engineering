from zero import _AsyncLogger

logger = _AsyncLogger()


async def log_message(
    msg: str,
):
    return await logger.log(msg)
