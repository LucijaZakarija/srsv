 Program je pisan u Pythonu na OS Windows.
 
 Program simulira rad lifta u zgradi od 4 kata. Na početku programa stvaraju se putnici koji se slučajno raspoređuju po katovima.Svi putnici su pripadnici klase putnik, imaju      definirano ime, početni i ciljni kat.
 Posebna dretva stvara putnike, osim nje postoje još dvije: lift i ispis. Ispis je ponmoćna dretva koja svaku s ispisuje trenutno stanje. Lift simulira kretanje lifta.
 Komunikacija između dretvi ostvarena je globalnim varijablama.
 Lift se kreće na poziv s određenog kata u smjeru poziva i pritom kupi sve putnike koji su poslali zahtjev u istom smjeru. Pri ulasku u lift putnik određuje kat na koji planira ići. Lift ima maksmialni kapacitet od 6 osoba, a na katu je max 10 osoba. 
