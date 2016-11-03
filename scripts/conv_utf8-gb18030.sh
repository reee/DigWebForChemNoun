find -name "*.csv" \
	-exec iconv -f utf8 -t gb18030 '{}' -o /tmp/iconv.tmp \; \
	-exec mv /tmp/iconv.tmp '{}' \;
