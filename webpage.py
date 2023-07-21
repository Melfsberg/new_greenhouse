def webpage(systime,tim,dur,cnt):
    
    html = f"""
    <!DOCTYPE html>
            <html>
                <head>
                <title>Bevattning</title>
                </head>                    
                
                <body>
                
                    <h1>Automatiskt bevattning</h1>
                        
                    <h5>System time {systime}</h4>
                    
                    <iframe src="http://free.timeanddate.com/clock/i8xv6ik4/n1377/tlse/th1" frameborder="0" width="57" height="18"></iframe>                          

                    
                    <form>
                    <label for="time1">Slinga 1:</label><br>
                    <input type="text" id="time1" name="time1" size=5 value={tim[0]}>
                    <input type="text" id="dur1"  name="dur1" size=3 style="text-align:right;" value={dur[0]} >
                    <input type="text" id="cnt1"  name="cnt1" size=3 style="text-align:right;" value={cnt[0]} readonly >
                    <button type="submit" formaction="/test1">Test1</button>
                    <br> 
                    
                    <label for="time2">Slinga 2:</label><br>
                    <input type="text" id="time2" name="time2" size=5 value={tim[1]}>
                    <input type="text" id="dur2"  name="dur2" size=3 style="text-align:right;" value={dur[1]} >
                    <input type="text" id="cnt2"  name="cnt2" size=3 style="text-align:right;" value={cnt[1]} readonly >
                    <button type="submit" formaction="/test2">Test2</button>
                    <br>
                    
                    <label for="time3">Slinga 3:</label><br>
                    <input type="text" id="time3" name="time3" size=5 value={tim[2]}>
                    <input type="text" id="dur3"  name="dur3" size=3 style="text-align:right;" value={dur[2]} >   
                    <input type="text" id="cnt3"  name="cnt3" size=3 style="text-align:right;" value={cnt[2]} readonly >
                    <button type="submit" formaction="/test3">Test3</button>
                    <br>
                    
                    <label for="time4">Slinga 4:</label><br>
                    <input type="text" id="time4" name="time4" size=5 value={tim[3]}>
                    <input type="text" id="dur4"  name="dur4" size=3 style="text-align:right;" value={dur[3]} >
                    <input type="text" id="cnt4"  name="cnt4" size=3 style="text-align:right;" value={cnt[3]} readonly >
                    <button type="submit" formaction="/test4">Test4</button>
                    <br>
                    
                    <br>
                    
                    <button type="submit" formaction="/URL1">Update</button>
                    <button type="submit" formaction="/time">Update Time</button>
                    <button type="submit" formaction="/reset">Reset</button>

                    <br>
           

                    </form>

                        
            </body>
            </html>
            """
        
    return html
