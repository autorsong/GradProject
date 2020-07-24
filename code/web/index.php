<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>텍스트 분석 기반의 상품 추천 시스템</title>

    <!-- 부트스트랩 -->
    <link href="bootstrap.min.css" rel="stylesheet">
		<style>
			.container{text-align: center; margin-top: 10px; width:40%;padding: 0px}
			.prod_frame{position: absolute; top: 0px; left: 0px}
			.radio{height: 30px; font-size: 22px; border-top: 3px solid #396190; padding-top: 10px}
			.row{margin:10px; cursor: pointer; height:130px; text-align: left; padding: 10px;border: 1px solid #396190;}
			.prod{font-weight: 900; color: #396190}
			img {width: 70px}
			.prod_name{margin-top: 10px}
			.prod_keyword{margin-top: 15px;}
			#colNotWord{display: none}
			.col-md-2{padding: 15px}
			iframe{
				transform: scale(0.15);
				transform-origin: 0 0;
			}
		</style>

    <!-- IE8 에서 HTML5 요소와 미디어 쿼리를 위한 HTML5 shim 와 Respond.js -->
    <!-- WARNING: Respond.js 는 당신이 file:// 을 통해 페이지를 볼 때는 동작하지 않습니다. -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
		<!-- jQuery (부트스트랩의 자바스크립트 플러그인을 위해 필요합니다) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
    <!-- 모든 컴파일된 플러그인을 포함합니다 (아래), 원하지 않는다면 필요한 각각의 파일을 포함하세요 -->
    <script src="bootstrap.min.js"></script>
  </head>
  <body>
		<div class="container">
			<?php
				$id = $_GET['id'];
			
				echo "<h1>".$id."님을 위한 맞춤 추천!</h1>";

				echo '<div class="radio"><label class="radio-inline"><input type="radio" name="inlineRadioOptions" id="withWord" value="option1" checked>검색단어 포함</label><label class="radio-inline"><input type="radio" name="inlineRadioOptions" id="withoutWord" value="option2">검색단어 미포함</label><div>';
			
			
				try {
					$m = new MongoClient('mongodb://127.0.0.1:27017');
					$db = $m->selectDB('test');
					$collection = new MongoCollection($db, 'final');
					$cursor = $collection->find(array('MBER_SEQ'=>$id));

					echo "<div id='colWord'>";
					foreach ($cursor as $document) {
						$product = $document["Product"];

						include_once "connect.php";
						$num = 0;
						foreach ($product as $product_num){
							$num += 1;
							$query = "select prod_nm, keyword from Product_info where prod_code = $product_num;";
							if (!($result = $connect->query($query))) throw new Exception($connect->error);
							$row = mysqli_fetch_array($result);
							
							$address = 'http://m.ssocio.com/mobile/prod/selectProd.do?PROD_CODE='.$product_num;
							
							$string = "<div class='row' id='$address'><div class='col-md-10'><h4 class='prod'>[추천 상품$num]</h4><h4 class='prod_name'>".$row['prod_nm']."</h4><h5 class='prod_keyword'>";
							
							$keyword = split(',', $row["keyword"]);
							for($c=0; $c<count($keyword); $c++){
								$string .= " #".$keyword[$c];
							}
							$string .= "</h5></div><div class='col-md-2'><img src='cursor.png'></div></div>";
							
							echo $string;
						}
					}
					echo "</div>";

				}
				catch (MongoException $e){
					echo "error message: ".$e->getMessage()."\n";
					echo "error code: ".$e->getCode()."\n";
				}

				try {
					$collection = new MongoCollection($db, 'final2');
					$cursor = $collection->find(array('MBER_SEQ'=>$id));

					echo "<div id='colNotWord'>";
					foreach ($cursor as $document) {
						$product = $document["Product"];

						include_once "connect.php";
						$num = 0;
						foreach ($product as $product_num){
							$num += 1;
							$query = "select prod_nm, keyword from Product_info where prod_code = $product_num;";
							if (!($result = $connect->query($query))) throw new Exception($connect->error);
							$row = mysqli_fetch_array($result);
							
							$address = 'http://m.ssocio.com/mobile/prod/selectProd.do?PROD_CODE='.$product_num;
							
							$string = "<div class='row' id='$address'><div class='col-md-10'><h4 class='prod'>[추천 상품$num]</h4><h4 class='prod_name'>".$row['prod_nm']."</h4><h5 class='prod_keyword'>";
							
							$keyword = split(',', $row["keyword"]);
							for($c=0; $c<count($keyword); $c++){
								$string .= " #".$keyword[$c];
							}
							$string .= "</h5></div><div class='col-md-2'><img src='cursor.png'></div></div>";
							
							echo $string;
						}
					}
					echo "</div>";

				}
				catch (MongoException $e){
					echo "error message: ".$e->getMessage()."\n";
					echo "error code: ".$e->getCode()."\n";
				}
			?>

			<script>
				$('.row').bind('click', function(){
					window.open(this.id);
				});

				$(document).ready(function(){ 
				    $("input:radio[name=inlineRadioOptions]").click(function(){ 
				        if($("#withWord").prop("checked")){
							$("#colWord").css("display", "block");
							$("#colNotWord").css("display", "none");
						}
						else if($("#withoutWord").prop("checked")){
							$("#colWord").css("display", "none");
							$("#colNotWord").css("display", "block");
						}
				    });
				});
			</script>
		</div>
  </body>
</html>