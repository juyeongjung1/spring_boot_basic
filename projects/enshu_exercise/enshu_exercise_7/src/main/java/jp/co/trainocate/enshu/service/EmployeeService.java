package jp.co.trainocate.enshu.service;

import java.util.List;

import jp.co.trainocate.enshu.entity.Employee;
import jp.co.trainocate.enshu.form.EmpForm;

/**
 * 従業員情報の操作（取得、登録、更新、削除）を定義するサービスインタフェースです。
 */
public interface EmployeeService {

    /**
     * 指定されたIDに対応する従業員情報を取得します。
     * @param id 従業員ID
     * @return 該当する従業員情報。該当しない場合はnullを返却します。
     */
    Employee findEmployeeById(int id);
    
    /**
     * 全従業員の情報を取得します。
     * @return 全従業員のリスト
     */
    List<Employee> findAllEmployees();
    
   
    
    /**
     * 従業員情報を新規登録または更新します。
     * @param empForm 従業員情報が格納されたフォーム
     */
    void saveEmployee(EmpForm empForm);
    
    /**
     * 指定されたIDの従業員情報を削除します。
     * @param id 削除対象の従業員ID
     */
    void deleteEmployee(int id);
}

