for /d %%D in (log-*) do (
	cd %%D\apps
	echo %CD%
	for /d %%d in (*.*) do (
    		cd %%d
		ren *.log *.txt
		copy *.txt *.csv
		cd ..
	)
	 cd ..\..
)
pause