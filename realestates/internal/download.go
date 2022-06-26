package internal

import (
	"io"
	"net/http"
)

// DlContent Download contents from specified url
func DlContent(requestUrl string, header map[string]string) []byte {
	client := &http.Client{}
	req, err := http.NewRequest(
		"GET",
		requestUrl,
		nil,
	)
	Check(err)

	if len(header) > 0 {
		for k, v := range header {
			req.Header.Add(k, v)
		}
	}

	resp, err := client.Do(req)
	Check(err)
	defer resp.Body.Close()

	contents, err := io.ReadAll(resp.Body)
	Check(err)

	return contents
}
