from property import ListingStatus, WaterfrontType

status = ListingStatus.ACTIVE
waterfront = WaterfrontType.WATERFRONT

print(status)
print(status.value)

print(status == ListingStatus.ACTIVE)
print(status == "active")

print(waterfront == WaterfrontType.INLAND)