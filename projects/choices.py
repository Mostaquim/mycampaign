CURRENCY = (
    (1, '£'),
)

STATUS = (
    (1, 'Sent'),
    (2, 'Open'),
    (3, 'Paid'),
    (4, 'Partially paid'),
    (5, 'Cancelled'),
)

PRIORITY = (
    (1, 'Low'),
    (2, 'Normal'),
    (3, 'High'),
    (4, 'Urgent'),
)

INVOICE_TERMS = '<div>Thank you for your business.' \
    ' P<span style="line-height: 1.42857;">lease process' \
    'this invoice in accordance with our agreement in order'  \
    'to avoid any&nbsp;</span><span style="line-height: 1.42857;">' \
    'interruption with your campaign start date. ASA Distribution is' \
    'the trading name of Marketize Ltd registered in England and ' \
    'Wales with company number&nbsp;</span>08277639, VAT Registration: ' \
    'GB228688464.</div><div><span style="font-size: 18px;">HOW TO PAY</span>' \
    '</div><div>Account Name: Marketize LTD</div><div>Bank Name: Natwest ' \
    'Bank </div><div>Sort Code: 60-21-02</div><div>' \
    'Account Number: 48203629</div>'


PROJECT_STATUS = (
    (1, "Not Started"),  # ns
    (2, "In Progress"),  # inp
    (3, "Completed"),  # cp
    (4, "Awaiting Payment"),  # ap
    (5, "Suspended"),  # sus
    (6, "Cancelled"),  # can
)
