select count(distinct item.seller) numSellersRatingAbv1000
from item, person
where item.seller = person.id
and person.rating > 1000;