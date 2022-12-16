import time


class Progress:

    def __init__(self):
        self.difference_now = time.time()

    def progress(self, count, total, now, command, message='In progress...', ):
        difference = time.time() - self.difference_now
        if difference > 15 or count in [1, total]:
            self.difference_now = time.time()

            remaining_time = self.time_definition(
                int((total / (count / (time.time() - now))) - (time.time() - now))
            )
            passed_time = self.time_definition(int(time.time() - now))
            command.stdout.write(command.style.MIGRATE_HEADING(
                "\r{} |{}{}| {}% | {} | {} left."
                .format(
                    message,
                    "█" * int(25 * count / total),
                    " " * (25 - int(25 * count / total)),
                    int(100 * count / total),
                    passed_time,
                    remaining_time
                )
            ))
            command.stdout.flush()

    def time_definition(self, time_input):
        try:
            time_input = int(time_input)
        except:
            pass
        if time_input >= 60 * 60 * 24:
            remaining = time_input % (60 * 60 * 24)
            day = int(time_input / (60 * 60 * 24))
            hour = int(remaining / (60 * 60))
            minute = int(int(remaining / 60) % 60)
            second = int(remaining % 60)

            if day > 99:
                final_time_string = '99+ day %s h %s min %s s' % (hour, minute, second)
            else:
                if not second:
                    if not minute:
                        if not hour:
                            final_time_string = '%s day' % (day)
                        else:
                            final_time_string = '%s day %s h' % (day, hour)
                    else:
                        final_time_string = '%s day %s h %s min' % (day, hour, minute)
                else:
                    final_time_string = '%s day %s h %s min %s s' % (day, hour, minute, second)
        elif time_input >= 60 * 60:
            remaining = time_input % (60 * 60)
            hour = int(time_input / (60 * 60))
            minute = int(remaining / 60)
            second = int(remaining % 60)
            if not second:
                if not minute:
                    final_time_string = '%s h' % (hour)
                else:
                    final_time_string = '%s h %s min' % (hour, minute)
            else:
                final_time_string = '%s h %s min %s s' % (hour, minute, second)
        elif time_input >= 60:
            minute = int(time_input / 60)
            second = int(time_input % 60)
            if not second:
                final_time_string = '%s min' % (minute)
            else:
                final_time_string = '%s min %s s' % (minute, second)
        else:
            final_time_string = '%s s' % (time_input)
        return final_time_string
