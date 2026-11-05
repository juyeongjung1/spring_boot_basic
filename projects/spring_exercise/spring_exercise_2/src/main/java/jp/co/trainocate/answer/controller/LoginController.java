package jp.co.trainocate.answer.controller;

//【ここにアノテーションを付けてください】
public class LoginController {

	// 【ここに「/login」というURLのマッピングをしてください 】
	public String showLoginView() {

		return "";//【ここに「login_input.html」を呼び出してください】

	}

	//【ここに、Post形式で「login」というURLのマッピングをしてください】
	public String doLogin() { 
		            // 【↑ここにint idと、String passwordを記載】)
			//System.out.println(id); 【//を削除してください】
			//System.out.println(password); 【//を削除してください】
			
		return "index";
	}
}
