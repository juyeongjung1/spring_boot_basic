package jp.co.trainocate.enshu.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;

import jp.co.trainocate.enshu.entity.Employee;
import jp.co.trainocate.enshu.entity.Location;
import jp.co.trainocate.enshu.form.EmpForm;
import jp.co.trainocate.enshu.repository.EmpRepository;
import jp.co.trainocate.enshu.repository.LocationRepository;

@Controller
public class EmpController {
	@Autowired
	private EmpRepository empRepo;

	@Autowired
	private LocationRepository locRepo;

	@GetMapping("/")
	public String index() {
		return "index";
	}

	//演習6.2-a
	//Employee全件検索メソッドを実装してください。

	@GetMapping("/findAll")
	public String findAll(Model model) {

		return "emp_list";
	}

	//演習6.3-b
	//社員番号で1人分の情報を取得し、"emp"としてModelに格納し、emp.htmlに遷移してください。
	@GetMapping("/showFindById")
	public String showFindById(int id, Model model) {

		return "emp";
	}

	//演習6.4-a
	//存在しない(null)id検索を行い、"emp"としてModelに格納し、emp2.htmlに遷移してください。
	@GetMapping("/showFindByIdSafe")
	public String showFindByIdSafe(int id, Model model) {

		return "emp2";
	}

	//演習6.5-a <select> を表示するためのlocationリストを取得してください。
	//"locations" という名前でModelに格納し、emp_input.html へ遷移してください。
	@GetMapping("/showInputView")
	public String showInputView(Model model) {
		
		
		return "emp_input";
	}

	//演習6.5-d
	@PostMapping("/insertEmp")
	public String insertEmp(EmpForm empForm, Model model) {

		// Employeeのエンティティをnewで生成し、
		// empFormからのデータを空っぽのEntityにコピーしてください。
		Employee emp = new Employee();
		emp.setName(empForm.getName());
		emp.setPassword(empForm.getPassword());
		emp.setSalary(empForm.getSalary());

		//employeeエンティティに移動し、locationIdフィールドを定義してから戻ってください。
		//直接setLocation()ではなく、setLocationId()を使ってください。

		//empRepoを使って、DBに保存してください。
		//save()メソッドを呼び出し、empに代入してください。
		//modelに"emp"というキーで保存したempを格納してください。

		return "result";
	}

	//演習6.6-a 以下のコードを確認してください。その後、emp_search.htmlも確認してください。
		@GetMapping("/showSearchForm")
		public String showSearchForm(Model model) {
		    List<Location> list = locRepo.findAll();
		    model.addAttribute("locationList", list);
		    return "emp_search";
		}

		//演習6.6.d
	    //emp_search.htmlから送られたデータを取得します。URLは /findHighSalary）
	    //引数に、給与（int salary）、勤務地名（String locationName）、Model model を指定します。
	    //EmpRepositoryのfindHighSalaryByLocationメソッドを呼び出し、取得結果をListに格納してください。
	    //取得したリストをmodelに"empList"というキー名で格納してください。
	    //emp_list.htmlを表示するようにreturnしてください。
		
		@GetMapping("/findHighSalary")
		public String findHighSalary(int salary, String locationName, Model model) {
		   
		    
		    return "emp_list";
		}
		
	@GetMapping("/delete/{id}")
	public String deleteEmp(@PathVariable int id) {
		empRepo.deleteById(id);
		return "redirect:/findAll";
	}
}
