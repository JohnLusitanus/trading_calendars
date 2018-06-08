from datetime import time
from itertools import chain
import pandas as pd
from pandas.tseries.holiday import (
    Holiday,
    DateOffset,
    MO,
    weekend_to_monday,
    GoodFriday
)
from pytz import timezone

from zipline.utils.calendars.trading_calendar import (
    TradingCalendar,
    HolidayCalendar,
    MONDAY,
    TUESDAY,
    WEDNESDAY,
    THURSDAY,
    FRIDAY,
)
from zipline.utils.calendars.exchange_calendar_lse import (
    Christmas,
    WeekendChristmas,
    BoxingDay,
    WeekendBoxingDay
)


# New Year's Day
TSXNewYearsDay = Holiday(
    "New Year's Day",
    month=1,
    day=1,
    observance=weekend_to_monday,
)
# Ontario Family Day
FamilyDay = Holiday(
    "Family Day",
    month=2,
    day=1,
    offset=DateOffset(weekday=MO(3)),
    start_date='2008-01-01',
)
# Victoria Day
VictoriaDay = Holiday(
    'Victoria Day',
    month=5,
    day=25,
    offset=DateOffset(weekday=MO(-1)),
)
# Canada Day
CanadaDay = Holiday(
    'Canada Day',
    month=7,
    day=1,
    observance=weekend_to_monday,
)
# Civic Holiday
CivicHoliday = Holiday(
    'Civic Holiday',
    month=8,
    day=1,
    offset=DateOffset(weekday=MO(1)),
)
# Labor Day
LaborDay = Holiday(
    'Labor Day',
    month=9,
    day=1,
    offset=DateOffset(weekday=MO(1)),
)
# Canadian Thanksgiving
CanadianThanksgiving = Holiday(
    'Canadian Thanksgiving',
    month=10,
    day=1,
    offset=DateOffset(weekday=MO(2)),
)

ChristmasEveEarlyClose2010Onwards = Holiday(
    'Christmas Eve Early Close',
    month=12,
    day=24,
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY),
    start_date=pd.Timestamp("2010-01-01"),
)

September11ClosingsCanada = pd.date_range('2001-09-11', '2001-09-12', tz='UTC')


class TSXExchangeCalendar(TradingCalendar):
    """
    Exchange calendar for the Toronto Stock Exchange

    Open Time: 9:30 AM, EST
    Close Time: 4:00 PM, EST

    Regularly-Observed Holidays:
    - New Years Day (observed on first business day on/after)
    - Family Day (Third Monday in February, starting in 2008)
    - Good Friday
    - Victoria Day (Monday before May 25th)
    - Canada Day (July 1st, observed first business day after)
    - Civic Holiday (First Monday in August)
    - Labor Day (First Monday in September)
    - Thanksgiving (Second Monday in October)
    - Christmas Day
        - Dec. 26th if Chrismas is on a Sunday
        - Dec. 27th if Christmas is on a weekend
    - Boxing Day
        - Dec. 27th if Christmas is on a Sunday
        - Dec. 28th if Boxing Day is on a weekend

    Early closes:
    - Starting in 2010, if Christmas Eve falls on a weekday, the market
      closes at 1:00 pm that day. If it falls on a weekend, there is no
      early close.
    """

    regular_early_close = time(13)

    @property
    def name(self):
        return "TSX"

    @property
    def tz(self):
        return timezone('Canada/Atlantic')

    @property
    def open_time(self):
        return time(9, 31)

    @property
    def close_time(self):
        return time(16)

    @property
    def regular_holidays(self):
        return HolidayCalendar([
            TSXNewYearsDay,
            FamilyDay,
            GoodFriday,
            VictoriaDay,
            CanadaDay,
            CivicHoliday,
            LaborDay,
            CanadianThanksgiving,
            Christmas,
            WeekendChristmas,
            BoxingDay,
            WeekendBoxingDay
        ])

    @property
    def adhoc_holidays(self):
        # NOTE: change the name of this property
        return list(chain(
            September11ClosingsCanada
        ))

    @property
    def special_closes(self):
        return [
            (self.regular_early_close, HolidayCalendar([
                ChristmasEveEarlyClose2010Onwards
            ]))
        ]
