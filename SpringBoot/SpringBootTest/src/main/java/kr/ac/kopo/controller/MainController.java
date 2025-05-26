package kr.ac.kopo.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.servlet.ModelAndView;

@Controller
public class MainController {

	@GetMapping("/")
	public ModelAndView main() {
		ModelAndView mav = new ModelAndView();
		
		mav.addObject("msg", "Spring-boot로 부터~");
		
		mav.setViewName("main");
		
		return mav;
	}

}