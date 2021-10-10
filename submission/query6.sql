select count(distinct item.seller) numUsersBothSellerBidder
from person, item, bid
where person.id = item.seller
and person.id = bid.bidder