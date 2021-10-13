export SCONE_MODE=sim
cd /encrypted-backend
scone fspf create fspf.pb
scone fspf addr fspf.pb / --kernel / --not-protected
scone fspf addr fspf.pb /encrypted-backend --encrypted --kernel /encrypted-backend
scone fspf addf fspf.pb /encrypted-backend /backend /encrypted-backend
scone fspf encrypt fspf.pb > /backend/keytag
