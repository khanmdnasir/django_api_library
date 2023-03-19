from django import dispatch

ticket_log_task = dispatch.Signal()
ticket_email_send_task = dispatch.Signal()
ticket_comments_task = dispatch.Signal()