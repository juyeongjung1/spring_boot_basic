package jp.co.trainocate.enshu.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;

@Controller

//演習3.2 
//b. データベースからデータを取得したいため、Employeeテーブルを操作できる
//EmpRepositoryの「依存性の注入」を行ってください。
public class EmpController {

	
	//初期画面遷移用メソッド(修正不要)
	@GetMapping("/")
	public String index() {
		return "index";
	}

	@GetMapping("/findAll")
	public String findAll(Model model) {
		//c. EmpRepositoryを利用して、全件検索を行ってください。	
		
		//d. 取得したリストをHTMLに出力させるため、modelに"empList"のキー名でリストを格納してください。
		
		return "emp_list";
	}

	//演習3.3
	@GetMapping("/showFindById")
	//b. showFindByIdメソッドの引数に、name属性値を追記してください。
	public String showFindById(Integer id, Model model) {

		//c. EmpRepositoryを利用して、主キー検索を行ってください。
		//d. 取得した社員データをHTMLに出力させるため、modelに"emp"のキー名でオブジェクトを格納してください。
		return "emp";
	}

	//演習3.4
	@GetMapping("/showFindBySalary")

	//c. showFindBySalaryメソッドの引数に、a.のname属性値を追記してください。
	public String showFindBySalary(Model model) {

		//d. EmpRepositoryを利用して、主キーではない列(salary)検索を行ってください。

		//e. 取得したリストをHTMLに出力させるため、modelにリストを格納してください。
		return "emp_list";
	}

	//演習3.5【オプション】
	@GetMapping("/showFindByName")
	public String showFindByName(String name) {
		
		
		return "emp_list";
	}
	
	
	//演習3.6
	//a. 入力画面へ遷移するためのメソッド(修正不要)
	@GetMapping("/showInputView")
	public String showInputView() {
		return "emp_input";
	}

	@PostMapping("/insertEmp")
	//d. メソッドの引数に、EmpFormとModelを入れてください。
	public String insertEmp() {

		//e. Employeeのエンティティをnewで生成し、
		//   empFormからのデータを空っぽのEntityにコピーしてください。
		
		//f. EmpRepositoryの変数を利用して、saveメソッドを呼び出してください。
		
		//登録データを戻り値として取得し、modelに"emp"のキー名で格納してください。
		return "result";
	}

	//演習3.7【オプション】
	//b. delete 処理をするメソッドを実装してください。
	///削除ボタンの動的URLでidを取得し、削除処理を行ってください
	@GetMapping("/delete/{}")
	public String deleteEmp(int id) {

		return "redirect:/findAll";
	}

}
