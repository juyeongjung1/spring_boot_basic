package jp.co.trainocate.enshu;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class MondaiController {
	
	@GetMapping("/")
	public String index() {
		return "index";
	}
}
