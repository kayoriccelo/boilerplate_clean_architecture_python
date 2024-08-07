import sys


def send_email_error(exception: Exception):
    """
    Simulate sending an email when an exception occurs.

    Args:
        exception (Exception): The exception that was raised.

    """

    exc_type, exc_value, _ = sys.exc_info()
    trace = exception.__traceback__

    # TODO - Kayo: simulate sending email.
    print(f"""
        *****************************************************
        
        WARNING: Exception generated by the system.

        type               : {exc_type.__name__}
        message            : {exc_value.message if hasattr(exc_value, 'message') else ''}
        error              : {exc_value.error if hasattr(exc_value, 'error') else ''}
        tracking lines     : 
    """)

    while trace is not None:
        print(f"""
            -------------------------------------------------  
            ---> path and file name : {trace.tb_frame.f_code.co_filename}
            ---> line code          : {trace.tb_lineno}
            ---> method name        : {trace.tb_frame.f_code.co_name}
            -------------------------------------------------
        """)

        trace = trace.tb_next

    print(f"""
        *****************************************************
    """)
