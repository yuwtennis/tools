package internal

import (
	"golang.org/x/text/encoding/japanese"
	"golang.org/x/text/transform"
	"io"
	"strings"
)

func ShiftJisToUTF8(fromBytes []byte) []byte {
	encoded, err := io.ReadAll(
		transform.NewReader(
			strings.NewReader(string(fromBytes)),
			japanese.ShiftJIS.NewDecoder(),
		),
	)

	Check(err)

	return encoded
}
