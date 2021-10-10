select count(*) numAuctionsFourCats from 
    (select item, count(*) count
    from category
    group by item) num_categories
where num_categories.count = 4;