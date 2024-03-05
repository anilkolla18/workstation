#!/usr/bin/bash

. /opt/apps/asa/dpCLI/.creds

usage()
{
	echo "$0 DPHOST DOMAIN"
	echo "required:"
	echo exit
	DPHOST, DOMAIN"
}

if [[ "$#" == "0" ]];then
	usage
fi

DPHOST=$1
DOMAIN=$2
TMPFILE=/tmp/tempfile.dp
OUTFILE=/tmp/outfile.dp
TS=`date +%Y%m%d%H%MXS`

echo "dphost: $DPHOST"
echo "domain: $DOMAIN"

for host in ${DPHOST[*]};do
echo "===========Running on ${host}==========="
cat << EOF > $TMPFILE
$DP_USER_ID
$DP_PASSWORD
$DOMAIN
show version
exit
EOF
ssh -T $host < $TMPFILE 1 > $OUTFILE.$TS
cat $OUTFILE.$TS | grep Version | grep -iv build | xargs
rm $TMPFILE
rm $OUTFILE.$TS
echo ""
done
