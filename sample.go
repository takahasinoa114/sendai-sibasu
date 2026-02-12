package main

import (
	"encoding/csv"
	"fmt"
	"io"
	"os"
	"strings"
	"time"
)

type BusTime struct {
	ArrivalTime string
	ServiceID   string
}

func main() {
	targetStopID := "7021_10"
	now := time.Now()
	nowStr := now.Format("15:04:05")
	today := strings.ToLower(now.Weekday().String())

	fmt.Printf("【現在時刻】 %s (%s)\n", nowStr, today)
	fmt.Println("データを準備中...")

	activeServices := make(map[string]bool)
	cFile, err := os.Open("calendar.txt")
	if err != nil {
		fmt.Println("calendar.txt が見つかりません")
		return
	}
	cReader := csv.NewReader(cFile)
	cHeader, _ := cReader.Read()

	// 曜日が何列目にあるか探す
	col := -1
	for i, h := range cHeader {
		if strings.ToLower(h) == today {
			col = i
			break
		}
	}

	// 曜日が見つからなかった時
	if col == -1 {
		fmt.Printf("エラー: calendar.txt 内に曜日 '%s' が見つかりませんでした。列名を確認してください。\n", today)
		return
	}

	for {
		rec, err := cReader.Read()
		if err == io.EOF { break }
		if len(rec) > col && rec[col] == "1" {
			activeServices[rec[0]] = true
		}
	}
	cFile.Close()

	tripToService := make(map[string]string)
	tFile, _ := os.Open("trips.txt")
	tReader := csv.NewReader(tFile)
	tReader.Read()
	for {
		rec, err := tReader.Read()
		if err == io.EOF { break }
		if len(rec) >= 3 {
			tripToService[rec[2]] = rec[1]
		}
	}
	tFile.Close()

	var myBuses []BusTime
	sFile, _ := os.Open("stop_times.txt")
	sReader := csv.NewReader(sFile)
	sReader.Read()
	for {
		rec, err := sReader.Read()
		if err == io.EOF { break }
		if len(rec) >= 4 && rec[3] == targetStopID {
			tripID := rec[0]
			sID, exists := tripToService[tripID]
			if exists && activeServices[sID] {
				myBuses = append(myBuses, BusTime{
					ArrivalTime: rec[1],
					ServiceID:   sID,
				})
			}
		}
	}
	sFile.Close()

	fmt.Println("--- 次に到着予定のバス ---")

	count := 0
	for _, bus := range myBuses {
		if bus.ArrivalTime > nowStr {
			fmt.Printf("%s 仙台行き\n", bus.ArrivalTime[:5])
			count++
		}
		if count >= 5 { break }
	}

	if count == 0 {
		fmt.Println("本日の運行は終了しました。")
	}
}