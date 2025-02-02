document.addEventListener('DOMContentLoaded', function () {
    // 「すべて表示」ボタンを取得
    var showMoreButton = document.getElementById('show-more');
    if (!showMoreButton) {
        console.error("show-more ボタンが見つかりません");
        return;
    }

    // ボタンのクリックイベントを設定
    showMoreButton.addEventListener('click', function () {
        console.log("ボタンがクリックされました");

        // JSONデータを取得
        var dataElement = document.getElementById('all-stations-data');
        if (!dataElement) {
            console.error("all-stations-data が見つかりません");
            return;
        }

        console.log(dataElement.textContent);

        // JSONをパース
        var allStations;
        try {
            allStations = JSON.parse(dataElement.textContent);
        } catch (e) {
            console.error("JSONデータのパースに失敗しました:", e);
            return;
        }

        // 駅リストを取得して新しい駅を追加
        var stationsList = document.getElementById('stations-list');
        if (!stationsList) {
            console.error("stations-list が見つかりません");
            return;
        }

        allStations.forEach(function (station) {
            var stationItem = document.createElement('div');
            stationItem.classList.add('col-6', 'col-md-6', 'col-lg-6');
            stationItem.style.paddingLeft = '5px';
            stationItem.style.paddingRight = '5px';

            // URLを動的に生成
            var stationUrl = stationListUrlPrefix + '/' + station.id ;  // ここでURLを生成

            stationItem.innerHTML = `
                <ul class="list-unstyled mb-0">
                    <li>
                        <a href="${stationUrl}">
                            ${station.name} (${station.shop_count})
                        </a>
                    </li>
                </ul>
            `;
            stationsList.appendChild(stationItem);
        });

        // ボタンを非表示にする
        showMoreButton.style.display = 'none';
    });
});
