def created_recent_days(self, days, field):
    import datetime
    if not isinstance(days, int):
        raise ValueError('The value %s is not a valid positive integer'%days)

    fields = self.model._meta.get_field(field)
    print(fields)

    today = datetime.date.today()
    days_ago = today - datetime.timedelta(days)
    return self.f(self.model._meta.get_field(field)=(days_ago, today))
