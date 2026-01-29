from briefly.model.ticket import IssueType

# https://fonts.google.com/icons

PRIORITY_ICON = "\uf16a"  # fire

DUE_DATE_ICON = "\uf540"  # calendar with clock

FLAG_ICON = "\ue153"  # flag

ISSUE_TYPE_ICONS: dict[IssueType, str] = {
    IssueType.TASK: "\ue834",  # checkbox
    IssueType.IMPROVEMENT: "\ue8e5",  # arrow up
    IssueType.FEATURE: "\uec1c",  # bolt
    IssueType.BUG: "\ue868",  # bug
    IssueType.PROD_BUG: "\uf568",  # the bomb
}
